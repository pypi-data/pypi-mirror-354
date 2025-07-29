import asyncio
import logging
import signal
import sys
import time
from pathlib import Path
from typing import Optional, Dict, List, Any, Union

from playwright.async_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

# Configurar el logger
logger = logging.getLogger('whatsplay')
logger.setLevel(logging.INFO)

# Evitar múltiples manejadores si el módulo se importa varias veces
if not logger.handlers:
    handler = logging.FileHandler('/home/ubuntu/Whabot/time.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

from .base_client import BaseWhatsAppClient
from .wa_elements import WhatsAppElements
from .utils import show_qr_window, copy_file_to_clipboard
from .constants.states import State
from .constants import locator as loc
from .object.message import Message, FileMessage
import datetime

class Client(BaseWhatsAppClient):
    """
    Cliente de WhatsApp Web implementado con Playwright
    """
    def __init__(self,
                 user_data_dir: Optional[str] = None,
                 headless: bool = False,
                 locale: str = 'en-US',
                 auth: Optional[Any] = None):
        super().__init__(user_data_dir=user_data_dir, headless=headless, auth=auth)
        self.locale = locale
        self.poll_freq = 0.25
        self.wa_elements = None
        self.qr_task = None
        self.current_state = None
        self.unread_messages_sleep = 1  # Tiempo de espera para cargar mensajes no leídos
        self._shutdown_event = asyncio.Event()
        self._setup_signal_handlers()
        
    def _setup_signal_handlers(self):
        """Configura los manejadores de señales para un cierre limpio"""
        if sys.platform != 'win32':
            # En Windows, asyncio solo soporta add_signal_handler para SIGINT y SIGTERM
            for sig in (signal.SIGINT, signal.SIGTERM):
                try:
                    asyncio.get_event_loop().add_signal_handler(
                        sig, lambda s=sig: asyncio.create_task(self._handle_signal(s)))
                except (NotImplementedError, RuntimeError):
                    # Algunas plataformas pueden no soportar add_signal_handler
                    signal.signal(sig, lambda s, f: asyncio.create_task(self._handle_signal(s)))
        else:
            # En Windows, solo podemos manejar estas señales
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, lambda s, f: asyncio.create_task(self._handle_signal(s)))
    
    async def _handle_signal(self, signum):
        """Maneja las señales del sistema para un cierre limpio"""
        signame = signal.Signals(signum).name if hasattr(signal, 'Signals') else str(signum)
        print(f"\nRecibida señal {signame}. Cerrando limpiamente...")
        self._shutdown_event.set()
        await self.stop()
        sys.exit(0)

    @property
    def running(self) -> bool:
        """Check if client is running"""
        return getattr(self, '_is_running', False)

    async def stop(self):
        """Detiene el cliente y libera todos los recursos"""
        if not hasattr(self, '_is_running') or not self._is_running:
            return
            
        self._is_running = False
        
        try:
            # Cerrar página si existe
            if hasattr(self, '_page') and self._page:
                try:
                    await self._page.close()
                except Exception as e:
                    await self.emit("on_error", f"Error al cerrar la página: {e}")
                finally:
                    self._page = None
            
            # Llamar al stop del padre para limpiar el contexto y el navegador
            await super().stop()
            
            # Asegurarse de que el navegador se cierre
            if hasattr(self, '_browser') and self._browser:
                try:
                    await self._browser.close()
                except Exception as e:
                    await self.emit("on_error", f"Error al cerrar el navegador: {e}")
                finally:
                    self._browser = None
            
            # Detener Playwright si está activo
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                except Exception as e:
                    await self.emit("on_error", f"Error al detener Playwright: {e}")
                finally:
                    self.playwright = None
                    
        except Exception as e:
            await self.emit("on_error", f"Error durante la limpieza: {e}")
        finally:
            await self.emit("on_stop")
            self._shutdown_event.set()

    async def start(self) -> None:
        """Inicia el cliente y maneja el ciclo principal"""
        try:
            await super().start()
            self.wa_elements = WhatsAppElements(self._page)
            self._is_running = True
            
            # Iniciar el ciclo principal
            await self._main_loop()
            
        except asyncio.CancelledError:
            # Manejar cancelación de tareas
            await self.emit("on_info", "Operación cancelada")
            raise
            
        except Exception as e:
            await self.emit("on_error", f"Error en el bucle principal: {e}")
            raise
            
        finally:
            # Asegurarse de que todo se cierre correctamente
            await self.stop()
    async def _main_loop(self) -> None:
        """Implementación del ciclo principal con manejo de errores"""
        if not self._page:
            await self.emit("on_error", "No se pudo inicializar la página")
            return
            
        await self.emit("on_start")
        
        # Tarea para capturas de pantalla automáticas (opcional, comentado por defecto)
        # screenshot_task = asyncio.create_task(self._auto_screenshot_loop(interval=30))
        
        try:
            # Tomar captura inicial para depuración
            try:
                await self._page.screenshot(path="init_main.png", full_page=True)
            except Exception as e:
                await self.emit("on_warning", f"No se pudo tomar captura inicial: {e}")
                
            await self._run_main_loop()
            
        except asyncio.CancelledError:
            await self.emit("on_info", "Bucle principal cancelado")
            raise
            
        except Exception as e:
            await self.emit("on_error", f"Error en el bucle principal: {e}")
            raise
            
        finally:
            # Cancelar tareas pendientes
            # screenshot_task.cancel()
            # try:
            #     await screenshot_task
            # except asyncio.CancelledError:
            #     pass
            pass
    
    async def _run_main_loop(self) -> None:
        """Bucle principal de la aplicación"""
        qr_binary = None
        state = None
        last_qr_shown = None  # Guarda la última imagen QR mostrada

        while self._is_running and not self._shutdown_event.is_set():
            try:
                curr_state = await self._get_state()
                self.current_state = curr_state  # Actualizar la propiedad current_state

                if curr_state is None:
                    await asyncio.sleep(self.poll_freq)
                    continue

                if curr_state != state:
                    await self._handle_state_change(curr_state, state)
                    state = curr_state
                else:
                    await self._handle_same_state(curr_state, last_qr_shown)
                    
                await self.emit("on_tick")
                await asyncio.sleep(self.poll_freq)
                
            except asyncio.CancelledError:
                await self.emit("on_info", "Bucle principal cancelado")
                raise
                
            except Exception as e:
                await self.emit("on_error", f"Error en la iteración del bucle: {e}")
                await asyncio.sleep(1)  # Pequeña pausa para evitar bucles rápidos de error
                
                # Si el error persiste, intentar reconectar después de varios fallos
                if self._consecutive_errors > 5:  # Ajusta según sea necesario
                    await self.emit("on_warning", "Demasiados errores consecutivos, intentando reconectar...")
                    try:
                        await self.reconnect()
                        self._consecutive_errors = 0
                    except Exception as reconnect_error:
                        await self.emit("on_error", f"Error al reconectar: {reconnect_error}")
                        # Si la reconexión falla, salir del bucle
                        break
    
    async def _handle_state_change(self, curr_state, prev_state):
        """Maneja los cambios de estado"""
        if curr_state == State.AUTH:
            await self.emit("on_auth")

        elif curr_state == State.QR_AUTH:
            try:
                qr_code_canvas = await self._page.wait_for_selector(loc.QR_CODE, timeout=5000)
                qr_binary = await self._extract_image_from_canvas(qr_code_canvas)

                if qr_binary != self.last_qr_shown:
                    show_qr_window(qr_binary)
                    self.last_qr_shown = qr_binary

                await self.emit("on_qr", qr_binary)
            except PlaywrightTimeoutError:
                await self.emit("on_warning", "Tiempo de espera agotado para el código QR")
            except Exception as e:
                await self.emit("on_error", f"Error al procesar código QR: {e}")

        elif curr_state == State.LOADING:
            loading_chats = await self._is_present(loc.LOADING_CHATS)
            await self.emit("on_loading", loading_chats)

        elif curr_state == State.LOGGED_IN:
            await self.emit("on_logged_in")
            await self._handle_logged_in_state()
    
    async def _handle_same_state(self, state, last_qr_shown):
        """Maneja la lógica cuando el estado no ha cambiado"""
        if state == State.QR_AUTH:
            await self._handle_qr_auth_state(last_qr_shown)
        elif state == State.LOGGED_IN:
            await self._handle_logged_in_state()
    
    async def _handle_qr_auth_state(self, last_qr_shown):
        """Maneja el estado de autenticación QR"""
        try:
            qr_code_canvas = await self._page.query_selector(loc.QR_CODE)
            if qr_code_canvas:
                curr_qr_binary = await self._extract_image_from_canvas(qr_code_canvas)

                if curr_qr_binary != last_qr_shown:
                    show_qr_window(curr_qr_binary)
                    last_qr_shown = curr_qr_binary
                    await self.emit("on_qr_change", curr_qr_binary)
        except Exception as e:
            await self.emit("on_warning", f"Error al actualizar código QR: {e}")
    
    async def _handle_logged_in_state(self):
        """Maneja el estado de sesión iniciada"""
        try:
            # Intentar hacer clic en el botón Continue si está presente
            continue_button = await self._page.query_selector("button:has(div:has-text('Continue'))")
            if continue_button:
                await continue_button.click()
                await asyncio.sleep(1)
                return  # Salir después de manejar el botón Continue
                
            # Manejar chats no leídos
            unread_chats = await self._check_unread_chats()
            if unread_chats:
                await self.emit("on_unread_chat", unread_chats)
                
        except Exception as e:
            await self.emit("on_error", f"Error en estado de sesión iniciada: {e}")
    
    async def _check_unread_chats(self):
        """Verifica y devuelve los chats no leídos"""
        unread_chats = []
        try:
            unread_button = await self._page.query_selector(loc.UNREAD_CHATS_BUTTON)
            if unread_button:
                await unread_button.click()
                await asyncio.sleep(self.unread_messages_sleep)

                chat_list = await self._page.query_selector_all(loc.UNREAD_CHAT_DIV)
                if chat_list and len(chat_list) > 0:
                    chats = await chat_list[0].query_selector_all(loc.SEARCH_ITEM)
                    for chat in chats:
                        chat_result = await self._parse_search_result(chat, "CHATS")
                        if chat_result:
                            unread_chats.append(chat_result)
            
            # Volver a la vista de todos los chats
            all_button = await self._page.query_selector(loc.ALL_CHATS_BUTTON)
            if all_button:
                await all_button.click()
                
        except Exception as e:
            await self.emit("on_warning", f"Error al verificar chats no leídos: {e}")
            
        return unread_chats

        qr_binary = None
        state = None
        last_qr_shown = None  # Guarda la última imagen QR mostrada

        while self.running:
            curr_state = await self._get_state()
            self.current_state = curr_state  # Actualizar la propiedad current_state

            if curr_state is None:
                await asyncio.sleep(self.poll_freq)
                continue

            if curr_state != state:
                if curr_state == State.AUTH:
                    await self.emit("on_auth")

                elif curr_state == State.QR_AUTH:
                    try:
                        qr_code_canvas = await self._page.wait_for_selector(loc.QR_CODE, timeout=5000)
                        qr_binary = await self._extract_image_from_canvas(qr_code_canvas)

                        if qr_binary != last_qr_shown:
                            show_qr_window(qr_binary)
                            last_qr_shown = qr_binary

                        await self.emit("on_qr", qr_binary)
                    except PlaywrightTimeoutError:
                        print("⚠️ Timeout esperando QR.")

                elif curr_state == State.LOADING:
                    loading_chats = await self._is_present(loc.LOADING_CHATS)
                    await self.emit("on_loading", loading_chats)

                elif curr_state == State.LOGGED_IN:
                    await self.emit("on_logged_in")

                    try:
                        continue_button = await self._page.query_selector("button:has(div:has-text('Continue'))")
                        if continue_button:
                            await continue_button.click()
                            await asyncio.sleep(1)
                    except Exception as e:
                        print(f"⚠️ Error en 'Continue': {e}")
                        await self.emit("on_error", f"⚠️ Error al hacer clic en 'Continue': {e}")

                state = curr_state

            else:
                if curr_state == State.QR_AUTH:
                    try:
                        qr_code_canvas = await self._page.query_selector(loc.QR_CODE)
                        if qr_code_canvas:
                            curr_qr_binary = await self._extract_image_from_canvas(qr_code_canvas)

                            if curr_qr_binary != last_qr_shown:
                                show_qr_window(curr_qr_binary)
                                last_qr_shown = curr_qr_binary
                                await self.emit("on_qr_change", curr_qr_binary)
                    except Exception:
                        pass

                elif curr_state == State.LOGGED_IN:
                    unread_chats = []
                    try:
                        continue_button = await self._page.query_selector("button:has(div:has-text('Continue'))")
                        if continue_button:
                            await continue_button.click()
                            await asyncio.sleep(2)
                    except Exception as e:
                        await self.emit("on_error", f"⚠️ Error al hacer clic en 'Continue': {e}")

                    try:
                        unread_button = await self._page.query_selector(loc.UNREAD_CHATS_BUTTON)
                        if unread_button:
                            await unread_button.click()
                            await asyncio.sleep(self.unread_messages_sleep)

                            chat_list = await self._page.query_selector_all(loc.UNREAD_CHAT_DIV)
                            if chat_list and len(chat_list) > 0:
                                chats = await chat_list[0].query_selector_all(loc.SEARCH_ITEM)
                                for chat in chats:
                                    inner_text = await chat.inner_text()
                                    chat_result = await self._parse_search_result(chat, "CHATS")
                                    if chat_result:
                                        unread_chats.append(chat_result)
                                        await self.emit("on_unread_chat", [chat_result])
                        else:
                            print("ℹ️ No se encontró el botón de chats no leídos.")

                        all_button = await self._page.query_selector(loc.ALL_CHATS_BUTTON)
                        if all_button:
                            await all_button.click()

                    except Exception as e:
                        print(f"❌ Error buscando chats no leídos: {e} ({type(e)})")
                        await self.emit("on_error", f"Error checking unread chats: {e} ({type(e)})")

            await self.emit("on_tick")
            await asyncio.sleep(self.poll_freq)


    async def _get_state(self) -> Optional[State]:
        """Obtiene el estado actual de WhatsApp Web"""
        return await self.wa_elements.get_state()
    
    async def open(self, chat_name: str, close = True) -> bool:
        if not await self.wait_until_logged_in():
            await self.emit("on_error", "Cliente no logueado.")
            return False

        # Helper function to escape chat name for CSS selectors
        def escape_css_string(value: str) -> str:
            return value.replace('"', '\\"')

        # Helper function to escape chat name for XPath query
        def escape_xpath_string(value: str) -> str:
            if "'" in value and '"' in value:
                parts = value.split("'")
                return "concat('" + "', \"'\" , '".join(parts) + "')"
            elif "'" in value:
                return f'"{value}"'
            else:
                return f"'{value}'"

        escaped_chat_name_for_css = escape_css_string(chat_name)

        async def find_and_click_chat_in_list(name: str) -> bool:
            try:
                xpath_selector = f"//span[@title='{name}']"
                chat_element = await self._page.wait_for_selector(
                    f"xpath={xpath_selector}",
                    timeout=1000,
                    state='attached'
                )
                
                if chat_element and await chat_element.is_visible():
                    await chat_element.click(delay=10)
                    await asyncio.sleep(0.1)
                    return True
                return False
            except Exception:
                return False

        # Primero intentar directamente sin filtros (más rápido)
        if await find_and_click_chat_in_list(chat_name):
            return True

        # 2. Si no se encuentra, intentar con el buscador
        await self.emit("on_info", f"Buscando chat '{chat_name}'...")
        search_button = await self._page.query_selector(loc.SEARCH_BUTTON)
        if search_button and await search_button.is_visible():
            try:
                await search_button.click()
                search_input = await self._page.wait_for_selector(loc.SEARCH_INPUT, timeout=2000)
                if search_input:
                    # Limpiar el campo de búsqueda y escribir el nombre
                    await search_input.click(click_count=3)  # Seleccionar todo
                    await search_input.press('Backspace')
                    await search_input.type(chat_name)  # Escribir más lento para evitar errores
                    
                    # Esperar un momento para que aparezcan los resultados
                    await asyncio.sleep(0.5)
                    
                    # Intentar hacer clic en el resultado de búsqueda
                    if await find_and_click_chat_in_list(chat_name):
                        return True
                    
                    # Si no se pudo hacer clic directamente, intentar con el selector de resultados
                    xpath_safe_chat_name = escape_xpath_string(chat_name)
                    chat_list_item_selector = f"{loc.SEARCH_ITEM}[.//span[@title={xpath_safe_chat_name}]]"
                    
                    try:
                        chat_result_element = await self._page.wait_for_selector(
                            chat_list_item_selector, 
                            timeout=3000,  
                            state="visible"
                        )
                        if chat_result_element:
                            await chat_result_element.scroll_into_view_if_needed()
                            await chat_result_element.click()
                            await asyncio.sleep(0.5)  
                            return True
                    except Exception:
                        pass
                    
            except Exception as e:
                await self.emit("on_warning", f"Error en la búsqueda: {e}")
        
        # Si llegamos aquí, no se pudo abrir el chat
        await self.emit("on_error", f"No se pudo abrir el chat '{chat_name}'")
        try:
            await self._page.keyboard.press("Escape")  # Cerrar barra de búsqueda si está abierta
        except Exception:
            pass
        return False

    async def _is_present(self, selector: str) -> bool:
        """Verifica si un elemento está presente en la página"""
        try:
            element = await self._page.query_selector(selector)
            return element is not None
        except Exception:
            return False

    async def _extract_image_from_canvas(self, canvas_element) -> Optional[bytes]:
        """Extrae la imagen de un elemento canvas"""
        if not canvas_element:
            return None
        try:
            return await canvas_element.screenshot()
        except Exception as e:
            await self.emit("on_error", f"Error extracting QR image: {e}")
            return None
        
    async def _parse_search_result(self, element, result_type: str = "CHATS") -> Optional[Dict[str, Any]]:
        try:
            components = await element.query_selector_all("xpath=.//div[@role='gridcell' and @aria-colindex='2']/parent::div/div")
            count = len(components)

            unread_el = await element.query_selector(f"xpath={loc.SEARCH_ITEM_UNREAD_MESSAGES}")
            unread_count = await unread_el.inner_text() if unread_el else "0"

            if count == 3:
                span_title_0 = await components[0].query_selector(f"xpath={loc.SPAN_TITLE}")
                group_title = await span_title_0.get_attribute("title") if span_title_0 else ""

                datetime_children = await components[0].query_selector_all("xpath=./*")
                datetime_text = await datetime_children[1].text_content() if len(datetime_children) > 1 else ""

                span_title_1 = await components[1].query_selector(f"xpath={loc.SPAN_TITLE}")
                title = await span_title_1.get_attribute("title") if span_title_1 else ""

                info_text = (await components[2].text_content()) or ""
                info_text = info_text.replace("\n", "")


                return {
                    "type": result_type,
                    "group": group_title,
                    "name": title,
                    "last_activity": datetime_text,
                    "last_message": info_text,
                    "unread_count": unread_count,
                    "element": element
                }

            elif count == 2:
                span_title_0 = await components[0].query_selector(f"xpath={loc.SPAN_TITLE}")
                title = await span_title_0.get_attribute("title") if span_title_0 else ""

                datetime_children = await components[0].query_selector_all("xpath=./*")
                datetime_text = await datetime_children[1].text_content() if len(datetime_children) > 1 else ""

                info_children = await components[1].query_selector_all("xpath=./*")
                info_text = (await info_children[0].text_content() if len(info_children) > 0 else "") or ""
                info_text = info_text.replace("\n", "")


                return {
                    "type": result_type,
                    "name": title,
                    "last_activity": datetime_text,
                    "last_message": info_text,
                    "unread_count": unread_count,
                    "element": element
                }

            return None

        except Exception as e:
            print(f"Error parsing result: {e}")
            return None




    async def wait_until_logged_in(self, timeout: int = 60) -> bool:
        """Espera hasta que el estado sea LOGGED_IN o se agote el tiempo"""
        start = time.time()
        while time.time() - start < timeout:
            if self.current_state == State.LOGGED_IN:
                return True
            await asyncio.sleep(self.poll_freq)
        await self.emit("on_error", "Tiempo de espera agotado para iniciar sesión")
        return False

    async def search_conversations(self, query: str, close=True) -> List[Dict[str, Any]]:
        """Busca conversaciones por término"""
        if not await self.wait_until_logged_in():
            return []
        try:
            return await self.wa_elements.search_chats(query, close)
        except Exception as e:
            await self.emit("on_error", f"Search error: {e}")
            return []

    async def collect_messages(self) -> List[Union[Message, FileMessage]]:
        """
        Recorre todos los contenedores de mensaje (message-in/message-out) actualmente visibles
        y devuelve una lista de instancias Message o FileMessage.
        """
        resultados: List[Union[Message, FileMessage]] = []
        # Selector de cada mensaje en pantalla
        msg_elements = await self._page.query_selector_all(
            'div[class*="message-in"], div[class*="message-out"]'
        )

        for elem in msg_elements:
            file_msg = await FileMessage.from_element(elem)
            if file_msg:
                resultados.append(file_msg)
                continue

            simple_msg = await Message.from_element(elem)
            if simple_msg:
                resultados.append(simple_msg)

        return resultados

    async def download_all_files(self, carpeta: Optional[str] = None) -> List[Path]:
        """
        Llama a collect_messages(), filtra FileMessage y descarga cada uno.
        Devuelve lista de Path donde se guardaron.
        """
        if not await self.wait_until_logged_in():
            return []

        # Carpeta destino
        if carpeta:
            downloads_dir = Path(carpeta)
        else:
            downloads_dir = Path.home() / "Downloads" / "WhatsAppFiles"

        archivos_guardados: List[Path] = []
        mensajes = await self.collect_messages()
        for m in mensajes:
            if isinstance(m, FileMessage):
                ruta = await m.download(self._page, downloads_dir)
                if ruta:
                    archivos_guardados.append(ruta)
        return archivos_guardados

    async def download_file_by_index(self, index: int, carpeta: Optional[str] = None) -> Optional[Path]:
        """
        Descarga sólo el FileMessage en la posición `index` de la lista devuelta
        por collect_messages() filtrando por FileMessage.
        """
        if not await self.wait_until_logged_in():
            return None

        if carpeta:
            downloads_dir = Path(carpeta)
        else:
            downloads_dir = Path.home() / "Downloads" / "WhatsAppFiles"

        mensajes = await self.collect_messages()
        archivos = [m for m in mensajes if isinstance(m, FileMessage)]
        if index < 0 or index >= len(archivos):
            return None

        return await archivos[index].download(self._page, downloads_dir)

    async def send_message(self, chat_query: str, message: str) -> bool:
        """Envía un mensaje a un chat"""
        if not await self.wait_until_logged_in():
            return False

        try:
            await self.open(chat_query)
            await self._page.wait_for_selector(loc.CHAT_INPUT_BOX, timeout=10000)
            input_box = await self._page.wait_for_selector(loc.CHAT_INPUT_BOX, timeout=10000)
            if not input_box:
                await self.emit("on_error", "No se encontró el cuadro de texto para enviar el mensaje")
                return False

            await input_box.click()
            await input_box.fill(message)
            await self._page.keyboard.press("Enter")
            return True

        except Exception as e:
            await self.emit("on_error", f"Error al enviar el mensaje: {e}")
            return False
    async def send_file(self, chat_name, path):
        try:
            await self.open(chat_name)
            copy_file_to_clipboard(path)
            
            input_box = await self._page.wait_for_selector(loc.CHAT_INPUT_BOX, timeout=10000)
            await input_box.click()
            
            await self._page.keyboard.press('Control+v')
            await asyncio.sleep(2)  # async sleep para no bloquear
            
            await self._page.keyboard.press('Enter')
            return True
        except Exception as e:
            await self.emit("on_error", f"Error al enviar el mensaje: {e}")
            return False
            
    async def _auto_screenshot_loop(self, interval: int = 30):
        """
        Toma una captura de pantalla cada `interval` segundos mientras el cliente esté corriendo.
        """
        counter = 0
        while self.running:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/wa_{timestamp}_{counter}.png"
            try:
                Path("screenshots").mkdir(exist_ok=True)
                await self._page.screenshot(path=filename, full_page=True)
                await self.emit("on_info", f"Screenshot tomada: {filename}")
            except Exception as e:
                await self.emit("on_error", f"Error al tomar screenshot periódica: {e}")
            counter += 1
            await asyncio.sleep(interval)


        
