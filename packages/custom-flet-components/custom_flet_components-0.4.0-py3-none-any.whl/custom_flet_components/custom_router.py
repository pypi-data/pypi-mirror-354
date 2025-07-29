import re
import flet as ft
from urllib.parse import urlparse, parse_qs
import inspect
from typing import Callable, Dict, Optional

class Router:
    def __init__(self, default_route: str = "/"):
        self.routes = {}
        self.protected_routes = set()
        self.page: Optional[ft.Page] = None
        self.current_route: str = default_route
        self.is_authenticated: bool = False
        self.history: list[str] = []
        self.default_route: str = default_route
        self.middleware: list[Callable[[ft.Page, str], None]] = []

    def route(self, path: str, protected: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            if protected:
                self.protected_routes.add(path)
            return func
        return decorator

    def add_middleware(self, middleware_func: Callable[[ft.Page, str], None]):
        self.middleware.append(middleware_func)

    def attach(self, page: ft.Page):
        self.page = page
        self.is_authenticated = self.page.client_storage.get("is_authenticated") == "true"
        page.on_route_change = self._on_route_change
        page.on_view_pop = self._on_view_pop
        if self.page.route:
            self.history = [self.page.route]
            self._render_route(self.page.route)

    def login(self):
        self.is_authenticated = True
        self.page.client_storage.set("is_authenticated", "true")
        #self.go(self.default_route)

    def logout(self):
        self.is_authenticated = False
        self.page.client_storage.remove("is_authenticated")
        self.go(self.default_route)

    def go(self, route: str):
        if not self.page:
            raise RuntimeError("Router not attached to a page")
        self.current_route = route
        if self.history and self.history[-1] == route:
            return
        self.history.append(route)
        self.page.go(route)

    def pop(self, default_route: str = None):
        if not self.page:
            raise RuntimeError("Router not attached to a page")
        default_route = default_route or self.default_route
        if len(self.history) > 1:
            self.history.pop()
            previous_route = self.history[-1]
            self.current_route = previous_route
            self.page.go(previous_route)
        else:
            self.current_route = default_route
            self.page.go(default_route)

    def _on_view_pop(self, e: ft.ViewPopEvent):
        self.pop()

    def _on_route_change(self, e: ft.RouteChangeEvent):
        self._render_route(e.route)

    def _render_route(self, full_route: str):
        if not self.page:
            return

        for middleware in self.middleware:
            middleware(self.page, full_route)

        parsed = urlparse(full_route)
        path = parsed.path
        query_params = {k: v[0] if v else "" for k, v in parse_qs(parsed.query).items()}
        self.current_route = full_route

        # Update history: avoid duplicates and maintain stack
        if self.history and self.history[-1] != full_route:
            if full_route in self.history:
                idx = self.history.index(full_route)
                self.history = self.history[:idx + 1]
            else:
                self.history.append(full_route)
        elif not self.history:
            self.history.append(full_route)

        matched_route, path_params = self._match_route(path)

        if not matched_route:
            self.page.views.append(
                ft.View(
                    route=full_route,
                    controls=[
                        ft.AppBar(
                            leading=ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                icon_color="black",
                                on_click=lambda _: self.pop()
                            )
                        ),
                        ft.Text("404", color="black", size=80, weight="bold", text_align="center"),
                        ft.Text("Page Not Found", color="black", size=26, text_align="center"),
                    ],
                    spacing=0,
                    horizontal_alignment="center",
                    vertical_alignment="center",
                    padding=10
                )
            )
            self.page.update()
            return

        if matched_route in self.protected_routes and not self.is_authenticated and path != "/login":
            self.page.go(f"/login?next={full_route}")
            return

        view_func = self.routes[matched_route]
        all_params = {**path_params, **query_params}
        sig = inspect.signature(view_func)
        valid_params = {
            name: value
            for name, value in all_params.items()
            if name in sig.parameters and name != 'page'
        }

        try:
            content = view_func(self.page, **valid_params)
            if not self.page.views or self.page.views[-1].route != full_route:
                self.page.views.clear()
                if isinstance(content, ft.View):
                    self.page.views.append(content)
                else:
                    self.page.views.append(ft.View(route=full_route, controls=[content]))
        except Exception as e:
            self.page.views.append(
                ft.View(
                    route=full_route,
                    controls=[ft.Text(f"Error rendering route: {str(e)}", color="red")],
                )
            )
        self.page.update()

    def _match_route(self, path: str) -> tuple[Optional[str], Dict[str, str]]:
        for route_pattern, handler in self.routes.items():
            param_names = re.findall(r":(\w+)", route_pattern)
            regex_pattern = re.sub(r":(\w+)", r"([^/]+)", route_pattern)
            match = re.match(f"^{regex_pattern}/*$", path)
            if match:
                values = match.groups()
                params = dict(zip(param_names, values))
                return route_pattern, params
        return None, {}
    

# def main(page: ft.Page):
#     page.title = "Router Demo"
#     router = Router()

#     def middleware_logger(page: ft.Page, route: str):
#         print(f"Navigated to: {route}")

#     router.add_middleware(middleware_logger)

#     @router.route("/")
#     def home(page: ft.Page):
#         return ft.Column(
#             [
#                 ft.Text("Home Page", size=30),
#                 ft.ElevatedButton("Go to Profile", on_click=lambda _: router.go("/profile/123")),
#                 ft.ElevatedButton("Go to Dashboard", on_click=lambda _: router.go("/dashboard")),
#                 ft.ElevatedButton("Login", on_click=lambda _: router.login()),
#             ]
#         )

#     @router.route("/profile/:id")
#     def profile(page: ft.Page, id: str):
#         return ft.Column(
#             [
#                 ft.Text(f"Profile Page for User {id}", size=30),
#                 ft.ElevatedButton("Go Home", on_click=lambda _: router.go("/")),
#                 ft.ElevatedButton("Back", on_click=lambda _: router.pop()),
#             ]
#         )

#     @router.route("/dashboard", protected=True)
#     def dashboard(page: ft.Page):
#         return ft.Column(
#             [
#                 ft.Text("Dashboard (Protected)", size=30),
#                 ft.ElevatedButton("Logout", on_click=lambda _: router.logout()),
#                 ft.ElevatedButton("Go Home", on_click=lambda _: router.go("/")),
#             ]
#         )

#     @router.route("/login")
#     def login(page: ft.Page, next: str = None):
#         return ft.Column(
#             [
#                 ft.Text("Login Page", size=30),
#                 ft.ElevatedButton("Login", on_click=lambda _: router.login()),
#                 ft.Text(f"Redirect to: {next or '/'}"),
#             ]
#         )

#     router.attach(page)
#     page.update()

# if __name__ == "__main__":
#     ft.app(target=main)