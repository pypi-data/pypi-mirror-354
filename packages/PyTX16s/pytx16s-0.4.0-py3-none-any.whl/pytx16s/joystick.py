import hid
from contextlib import suppress
import logging
from typing import Literal

from models import DeviceReport, Device

ZERO_BYTE_CONDITIONS = {
    0: "",
    1: "e",
    2: "a",
    4: "d",
    8: "h",
    6: "ad",
    3: "ae",
    10: "ah",
    5: "de",
    12: "dh",
    9: "eh",
    7: "ade",
    14: "adh",
    11: "aeh",
    13: "deh",
    15: "ahde",
}
"""
A dictionary of switch status sums, for those switches that interact with the zero byte of the device report.
The keys are the sum of the switch states and reflect the size of the first byte. 
Values are sets of active switches.
"""


class Joystick:
    def __init__(
        self,
        device: hid.Device | None = None,
        device_model: Device | None = None,
        auto_connect: bool = True,
        auto_reconnect: bool = True,
    ):
        """Initialize the Joystick class.
        Args:
            device (hid.Device, optional): A specific HID device to connect to.
            auto_connect (bool, optional): Automatically connect to the device if not provided. Defaults to True.
            auto_reconnect (bool, optional): Automatically reconnect if the device is disconnected. Defaults to True.
        """
        self.device_model = device_model
        self._logger = logging.getLogger(__name__)
        self.connected = False
        self.device = device if device else self.connect() if auto_connect else None
        self.auto_reconnect = auto_reconnect

    def connect(
        self,
        device_model: Device | None = None,
        connect_mode: Literal["reconnect", "scan"] = "scan",
    ) -> Device:
        logging_mode = "debug" if connect_mode == "reconnect" else "info"

        getattr(self._logger, logging_mode)("Connecting to OpenTX device...")

        if (device_model or self.device_model) and not self.connected:
            getattr(self._logger, logging_mode)(
                f"Using provided device model: {device_model.product if device_model else self.device_model.product}"
            )
            self.device = hid.Device(
                vid=device_model.vendor_id
                if device_model
                else self.device_model.vendor_id,
                pid=device_model.product_id if device_model else self.device_model.product_id,
            )
            self.connected = True
            return self.device

        devices = [
            Device(
                vendor_id=device["vendor_id"],
                product_id=device["product_id"],
                path=device["path"],
                manufacturer=device["manufacturer_string"],
                product=device["product_string"],
                serial=device["serial_number"],
            )
            for device in hid.enumerate()
        ]
        for device in devices:
            if device.manufacturer.lower() == "opentx":
                getattr(self._logger, logging_mode)(
                    f"Found OpenTX device: {device.product}. Connecting..."
                )
                self.device_model = device
                self.device = hid.Device(vid=device.vendor_id, pid=device.product_id)
                self._logger.info(f"Successfully connected to {device.product}")
                self.connected = True
                return self.device

        if connect_mode == "scan":
            self._logger.info("Cannot find OpenTX device automatically")

            print("-----------------------")
            print("LIST OF HID DEVICES:")
            print("-----------------------")

            for index, device in enumerate(devices, 1):
                print(
                    f"[{index}] - Manufacturer: {device.manufacturer} | Product: {device.product}"
                )
            device_index = (
                int(input("Please, choose the device you want to connect to: ")) - 1
            )
            if 0 <= device_index < len(devices):
                selected_device = devices[device_index]

                self.device_model = selected_device
                self.device = hid.Device(
                    vid=selected_device.vendor_id, pid=selected_device.product_id
                )

                self._logger.info(
                    f"Successfully connected to {selected_device.product}"
                )
                self.connected = True

                return self.device

    def reconnect(self):
        """Reconnect to the OpenTX device."""
        self._logger.info("Reconnecting to OpenTX device...")
        while not self.connected:
            with suppress(hid.HIDException):
                self.device = self.connect(device_model=self.device_model, connect_mode="reconnect")
        self.connected = True

    def close(self):
        """Close the connection to the device."""
        if self.device:
            self.device.close()
            self.connected = False
            self._logger.info("Connection closed.")
        else:
            self._logger.warning("No device to close.")

    def get_device_report(self):
        try:
            report = self.device.read(19)
        except hid.HIDException as e:
            self._logger.error(f"Failed to read from device: {e}")
            self.connected = False
            if self.auto_reconnect:
                self.reconnect()
                report = self.device.read(19)
        
        left_stick_x = report[9] + 256 * report[10] - 1024
        left_stick_y = report[7] + 256 * report[8] - 1024
        right_stick_x = report[3] + 256 * report[4] - 1024
        right_stick_y = report[5] + 256 * report[6] - 1024

        switch_a = int("a" in ZERO_BYTE_CONDITIONS[report[0]]) * 2
        switch_d = int("d" in ZERO_BYTE_CONDITIONS[report[0]]) * 2
        switch_e = int("e" in ZERO_BYTE_CONDITIONS[report[0]]) * 2
        switch_h = int("h" in ZERO_BYTE_CONDITIONS[report[0]])

        switch_f = int(bool(report[11]))
        switch_b = int(bool(report[13]) + bool(report[14]))
        switch_c = int(bool(report[15]) + bool(report[16]))
        switch_g = int(bool(report[17]) + bool(report[18]))

        report = DeviceReport(
            left_stick_x,
            left_stick_y,
            right_stick_x,
            right_stick_y,
            switch_a,
            switch_d,
            switch_e,
            switch_h,
            switch_f,
            switch_b,
            switch_c,
            switch_g,
        )

        return report
