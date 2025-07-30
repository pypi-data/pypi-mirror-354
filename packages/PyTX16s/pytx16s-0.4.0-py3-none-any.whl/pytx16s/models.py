from dataclasses import dataclass


@dataclass
class Device:
    vendor_id: int
    product_id: int
    path: str
    manufacturer: str
    product: str
    serial: str


@dataclass
class DeviceReport:
    left_stick_x: int
    left_stick_y: int
    right_stick_x: int
    right_stick_y: int
    switch_a: int
    switch_d: int
    switch_e: int
    switch_h: int
    switch_f: int
    switch_b: int
    switch_c: int
    switch_g: int