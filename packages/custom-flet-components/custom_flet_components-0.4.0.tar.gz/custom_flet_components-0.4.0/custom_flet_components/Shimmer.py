import asyncio
from typing import Optional, Callable, Dict
import httpx
import flet as ft

class AnimationStyle:
    SLIDE = "slide"
    FADE = "fade"
    PULSE = "pulse"

class Shimmer(ft.Container):
    def __init__(
        self,
        ref: Optional[ft.Ref[ft.ShaderMask]] = None,
        control: Optional[ft.Control] = None,
        color: Optional[str] = None,
        color1: Optional[str] = None,
        color2: Optional[str] = None,
        light_shimmer_color: Optional[str] = None,
        light_shimmer_color1: Optional[str] = None,
        light_shimmer_color2: Optional[str] = None,
        dark_shimmer_color: Optional[str] = None,
        dark_shimmer_color1: Optional[str] = None,
        dark_shimmer_color2: Optional[str] = None,
        height: Optional[float] = None,
        width: Optional[float] = None,
        auto_generate: bool = False,
        original: bool = False,
        animation_speed: float = 0.02,
        animation_gap: float = 0.075,
        animation_delay: float = 0.03,
        reset_delay: float = 0.4,
        animation_style: str = AnimationStyle.SLIDE,
        dummy_templates: Optional[Dict[str, Callable[[ft.Control], ft.Control]]] = None,
        page: Optional[ft.Page] = None,
    ) -> None:
        super().__init__()
        self.page = page
        self.color = color
        self.color1 = color1
        self.color2 = color2
        self.light_shimmer_color = light_shimmer_color
        self.light_shimmer_color1 = light_shimmer_color1
        self.light_shimmer_color2 = light_shimmer_color2
        self.dark_shimmer_color = dark_shimmer_color
        self.dark_shimmer_color1 = dark_shimmer_color1
        self.dark_shimmer_color2 = dark_shimmer_color2
        self.height = height
        self.width = width
        self.ref = ref if ref else ft.Ref[ft.ShaderMask]()
        is_light = page and page.theme_mode == ft.ThemeMode.LIGHT
        self.__color1 = (
            light_shimmer_color or light_shimmer_color1 or color or color1
            if is_light
            else dark_shimmer_color or dark_shimmer_color1 or color or color1 or ft.Colors.BLUE_GREY_700
        ) or ft.Colors.BLUE_GREY_200
        self.__color2 = ft.Colors.with_opacity(
            0.5,
            (
                light_shimmer_color or light_shimmer_color2 or color or color2
                if is_light
                else dark_shimmer_color or dark_shimmer_color2 or color or color2 or ft.Colors.BLUE_GREY_800
            ) or ft.Colors.BLUE_GREY_300
        )
        self.dummy_templates = dummy_templates or {}
        self.original = original
        self.control = self.create_dummy(control) if auto_generate else control
        self.__stop_shine = False
        self.__paused = False
        self.i = -0.1
        self.gap = animation_gap
        self.animation_speed = animation_speed
        self.animation_delay = animation_delay
        self.reset_delay = reset_delay
        self.animation_style = animation_style
        self.build()

    def build(self) -> None:
        gradient = ft.LinearGradient(
            colors=[self.__color2, self.__color1, self.__color2],
            stops=[max(0, self.i - self.gap), self.i, min(1, self.gap + self.i)],
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
        )
        self.__shadermask = ft.ShaderMask(
            ref=self.ref,
            content=self.control,
            blend_mode=ft.BlendMode.DST_IN,
            height=self.height,
            width=self.width,
            shader=gradient,
        )
        self.content = self.__shadermask
        self.bgcolor = self.__color1

    async def shine_async(self) -> None:
        try:
            while not self.__stop_shine:
                if not self.__paused:
                    gradient = None
                    if self.animation_style == AnimationStyle.FADE:
                        opacity = 0.5 + 0.5 * (self.i % 1.0)
                        gradient = ft.LinearGradient(
                            colors=[
                                ft.Colors.with_opacity(opacity, self.__color2),
                                ft.Colors.with_opacity(opacity, self.__color1),
                                ft.Colors.with_opacity(opacity, self.__color2)
                            ],
                            stops=[0, 0.5, 1],
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                        )
                        self.i += self.animation_speed
                        if self.i >= 1.0:
                            self.i = 0
                    elif self.animation_style == AnimationStyle.PULSE:
                        scale = 1.0 + 0.05 * (self.i % 1.0)
                        gradient = ft.LinearGradient(
                            colors=[self.__color2, self.__color1, self.__color2],
                            stops=[max(0, self.i - self.gap), self.i, min(1, self.gap + self.i)],
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                        )
                        if self.ref.current:
                            self.ref.current.scale = scale
                        self.i += self.animation_speed
                        if self.i >= 1.0:
                            self.i = 0
                    else:  # SLIDE
                        gradient = ft.LinearGradient(
                            colors=[self.__color2, self.__color1, self.__color2],
                            stops=[max(0, self.i - self.gap), self.i, min(1, self.gap + self.i)],
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                        )
                        self.i += self.animation_speed
                        if self.i >= 1.1:
                            self.i = -0.1
                            await asyncio.sleep(self.reset_delay)
                    if self.ref.current and gradient:
                        self.ref.current.shader = gradient
                        self.ref.current.update()
                await asyncio.sleep(self.animation_delay)
        except Exception as e:
            print(f"Error in shine_async: {e}")

    def stop_shine(self) -> None:
        self.__stop_shine = True

    def pause_shimmer(self) -> None:
        self.__paused = True

    def resume_shimmer(self) -> None:
        self.__paused = False

    def create_dummy(self, target: Optional[ft.Control] = None) -> ft.Control:
        if target is None:
            return ft.Container(bgcolor=self.__color1)

        if getattr(target, "data", None) == "skip_shimmer":
            return target

        opacity = 0.1
        color = ft.Colors.ON_PRIMARY_CONTAINER

        circle = lambda size=60: ft.Container(
            height=size, width=size, bgcolor=ft.Colors.with_opacity(opacity, color), border_radius=size
        )
        rectangle = lambda height, content=None: ft.Container(
            content=content, height=height, width=height * 2.5, bgcolor=ft.Colors.with_opacity(opacity, color),
            border_radius=20, alignment=ft.alignment.bottom_center, padding=20
        )
        tube = lambda width: ft.Container(
            height=10, width=width, bgcolor=ft.Colors.with_opacity(opacity, color), border_radius=20, expand=0
        )

        dummy = None
        ctrl_name = target._get_control_name() if hasattr(target, "_get_control_name") else ""

        if self.original:
            try:
                dummy = type(target)()
            except Exception as e:
                print(f"Error creating control type {ctrl_name}: {e}")
                dummy = ft.Container(bgcolor=self.__color1)
        else:
            if getattr(target, "data", None) == "shimmer_load" and ctrl_name in self.dummy_templates:
                dummy = self.dummy_templates[ctrl_name](target)
            elif getattr(target, "data", None) == "shimmer_load":
                if ctrl_name == "text":
                    text_value = target._Control__attrs.get("value", [None])[0]
                    dummy = tube(len(text_value) * 7.5 if isinstance(text_value, str) else 100)
                elif ctrl_name == "textbutton":
                    dummy = rectangle(40)
                elif ctrl_name == "icon":
                    dummy = circle(30)
                elif ctrl_name == "image":
                    dummy = ft.Container(bgcolor=ft.Colors.with_opacity(opacity, color), expand=True)
                elif ctrl_name == "container":
                    dummy = ft.Container(
                        bgcolor=ft.Colors.with_opacity(opacity, target.bgcolor or color),
                        width=target.width,
                        height=target.height,
                        padding=target.padding,
                        border=target.border,
                        border_radius=target.border_radius,
                        alignment=target.alignment,
                    )
                elif ctrl_name == "column":
                    dummy = ft.Column(
                        spacing=target.spacing,
                        alignment=target.alignment,
                        horizontal_alignment=target.horizontal_alignment,
                    )
                else:
                    try:
                        dummy = type(target)()
                    except Exception as e:
                        print(f"Error creating control type {ctrl_name}: {e}")
                        dummy = ft.Container(bgcolor=self.__color1)

        if dummy is None:
            print(f"Warning: Dummy control is None for {ctrl_name}, using fallback")
            dummy = ft.Container(bgcolor=self.__color1)

        ctrl_attrs = getattr(target, "_Control__attrs", {})
        for attr_name, attr_value in ctrl_attrs.items():
            if self.original or attr_name not in [
                "text", "value", "label", "foregroundimageurl", "bgcolor", "name", "color", "icon", "src", "src_base64"
            ]:
                try:
                    dummy._set_attr(attr_name, attr_value[0])
                except Exception as e:
                    print(f"Failed to set attribute {attr_name} on dummy: {e}")

        for key in target.__dict__:
            value = target.__dict__[key]
            if value is not None:
                pos = key.split("__")[-1]
                try:
                    if pos == "rotate":
                        dummy.rotate = value
                    elif pos == "scale":
                        dummy.scale = value
                    elif pos == "border_radius":
                        dummy.border_radius = value
                    elif pos == "alignment":
                        dummy.alignment = value
                    elif pos == "padding":
                        dummy.padding = value
                    elif pos == "horizontal_alignment":
                        dummy.horizontal_alignment = value
                    elif pos == "vertical_alignment":
                        dummy.vertical_alignment = value
                    elif pos == "top":
                        dummy.top = value
                    elif pos == "bottom":
                        dummy.bottom = value
                    elif pos == "left":
                        dummy.left = value
                    elif pos == "right":
                        dummy.right = value
                    elif pos == "width":
                        dummy.width = value
                    elif pos == "height":
                        dummy.height = value
                    elif pos == "expand":
                        dummy.expand = value
                    elif pos == "spacing" and isinstance(dummy, ft.Column):
                        dummy.spacing = value
                    elif pos == "border":
                        dummy.border = value
                    elif pos == "rows":
                        dummy.rows = [
                            ft.DataRow(
                                [ft.DataCell(self.create_dummy(cell.content) if getattr(cell.content, "data", None) != "skip_shimmer" else cell.content)
                                 for cell in row.cells]
                            ) for row in value
                        ]
                    elif pos == "columns":
                        dummy.columns = [
                            ft.DataColumn(self.create_dummy(col.label) if getattr(col.label, "data", None) != "skip_shimmer" else col.label)
                            for col in value
                        ]
                except Exception as e:
                    print(f"Error setting property {pos} on dummy: {e}")

        if hasattr(target, "content") and target.content:
            dummy.content = self.create_dummy(target.content)
        if hasattr(target, "title") and target.title:
            dummy.title = self.create_dummy(target.title)
        if hasattr(target, "subtitle") and target.subtitle:
            dummy.subtitle = self.create_dummy(target.subtitle)
        if hasattr(target, "leading") and target.leading:
            dummy.leading = self.create_dummy(target.leading)
        if hasattr(target, "trailing") and target.trailing:
            dummy.trailing = self.create_dummy(target.trailing)
        if hasattr(target, "controls") and target.controls:
            dummy.controls = []
            for ctrl in target.controls:
                try:
                    dummy_control = self.create_dummy(ctrl)
                    if dummy_control is not None:
                        dummy.controls.append(dummy_control)
                    else:
                        print(f"Warning: Skipping None control in {ctrl_name}")
                except Exception as e:
                    print(f"Failed to create dummy for control {ctrl}: {e}")

        if not self.original and getattr(target, "data", None) == "shimmer_load" and not isinstance(dummy, (ft.Container, ft.Column, ft.Text, ft.TextButton, ft.Icon, ft.Image)):
            dummy.bgcolor = ft.Colors.with_opacity(opacity, color)

        return dummy if self.original or isinstance(dummy, (ft.Container, ft.Column)) else ft.Container(ft.Stack([dummy]), bgcolor=self.__color1)

    def did_mount(self) -> None:
        if self.page:
            self.task = self.page.run_task(self.shine_async)

    def will_unmount(self) -> None:
        self.stop_shine()
        if hasattr(self, "task"):
            self.task.cancel()

class ShimmerWidget(ft.Container):
    def __init__(
        self,
        control: ft.Control,
        page: ft.Page,
        loading_duration: float = 3.0,
        shimmer_color: Optional[str] = None,
        shimmer_color1: Optional[str] = None,
        shimmer_color2: Optional[str] = None,
        light_shimmer_color: Optional[str] = None,
        light_shimmer_color1: Optional[str] = None,
        light_shimmer_color2: Optional[str] = None,
        dark_shimmer_color: Optional[str] = None,
        dark_shimmer_color1: Optional[str] = None,
        dark_shimmer_color2: Optional[str] = None,
        animation_style: str = AnimationStyle.SLIDE,
        dummy_templates: Optional[Dict[str, Callable[[ft.Control], ft.Control]]] = None,
        original: bool = False,
        on_start: Optional[Callable[[], None]] = None,
        on_complete: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__()
        self.control = self._mark_shimmer_data(control, include_parent=True)
        self.page = page
        self.loading_duration = loading_duration
        self.on_start = on_start
        self.on_complete = on_complete
        self.content = Shimmer(
            control=self.control,
            auto_generate=True,
            color=shimmer_color,
            color1=shimmer_color1,
            color2=shimmer_color2,
            light_shimmer_color=light_shimmer_color,
            light_shimmer_color1=light_shimmer_color1,
            light_shimmer_color2=light_shimmer_color2,
            dark_shimmer_color=dark_shimmer_color,
            dark_shimmer_color1=dark_shimmer_color1,
            dark_shimmer_color2=dark_shimmer_color2,
            animation_style=animation_style,
            dummy_templates=dummy_templates,
            original=original,
            page=page,
        )
        if self.page:
            self.page.run_task(self._show)

    def _mark_shimmer_data(self, control: ft.Control, include_parent: bool = False) -> ft.Control:
        if include_parent and hasattr(control, "data") and control.data != "skip_shimmer":
            control.data = "shimmer_load"
        if hasattr(control, "content") and control.content:
            self._mark_shimmer_data(control.content, include_parent=True)
        if hasattr(control, "controls") and control.controls:
            for ctrl in control.controls:
                self._mark_shimmer_data(ctrl, include_parent=True)
        return control

    async def _show(self) -> None:
        if self.on_start:
            self.on_start()
        if self.page:
            self.page.update()
        await asyncio.sleep(self.loading_duration)
        self.content = self.control
        if self.page:
            self.page.update()
        if self.on_complete:
            self.on_complete()

    async def start_shimmer(self) -> None:
        self.content = Shimmer(
            control=self._mark_shimmer_data(self.control, include_parent=True),
            auto_generate=True,
            color=self.content.color if isinstance(self.content, Shimmer) else None,
            color1=self.content.color1 if isinstance(self.content, Shimmer) else None,
            color2=self.content.color2 if isinstance(self.content, Shimmer) else None,
            light_shimmer_color=self.content.light_shimmer_color if isinstance(self.content, Shimmer) else None,
            light_shimmer_color1=self.content.light_shimmer_color1 if isinstance(self.content, Shimmer) else None,
            light_shimmer_color2=self.content.light_shimmer_color2 if isinstance(self.content, Shimmer) else None,
            dark_shimmer_color=self.content.dark_shimmer_color if isinstance(self.content, Shimmer) else None,
            dark_shimmer_color1=self.content.dark_shimmer_color1 if isinstance(self.content, Shimmer) else None,
            dark_shimmer_color2=self.content.dark_shimmer_color2 if isinstance(self.content, Shimmer) else None,
            animation_style=self.content.animation_style if isinstance(self.content, Shimmer) else AnimationStyle.SLIDE,
            dummy_templates=self.content.dummy_templates if isinstance(self.content, Shimmer) else None,
            original=self.content.original if isinstance(self.content, Shimmer) else False,
            page=self.page,
        )
        if self.page:
            self.page.update()
            self.page.run_task(self._show)

    async def stop_shimmer(self) -> None:
        if isinstance(self.content, Shimmer):
            self.content.stop_shine()
        self.content = self.control
        if self.page:
            self.page.update()