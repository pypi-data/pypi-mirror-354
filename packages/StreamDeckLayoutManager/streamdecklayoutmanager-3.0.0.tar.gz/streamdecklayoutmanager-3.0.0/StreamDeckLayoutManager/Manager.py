#
# Copyright (c) 2022-present Didier Malenfant <didier@malenfant.net>
#
# This file is part of StreamDeckLayoutManager.
#
# StreamDeckLayoutManager is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# StreamDeckLayoutManager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with StreamDeckLayoutManager. If not,
# see <https://www.gnu.org/licenses/>.
#

import os
import sys

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from StreamDeck.Devices import StreamDeck
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any, Callable

from .CallbackCall import CallbackCall


# -- Classes
class KeyConfig:
    """Configuration for a given key."""

    def __init__(self, image: Optional[str] = None, label: Optional[str] = None):
        self.image: str = '' if image is None else image
        self.label: str = '' if label is None else label
        self.margins: List[int] = []
        self.pressed_callbacks: List[CallbackCall] = []
        self.released_callbacks: List[CallbackCall] = []


class Manager:
    """Manage all our Stream Deck interactions."""

    def __init__(self, config_file_path: str, deck_index: int = 0):
        """Initialize the manager based on user configuration."""

        self._key_configs: Dict[str, KeyConfig] = {}
        self._assets_folder: Optional[str] = None
        self._font: Optional[ImageFont.FreeTypeFont] = None
        self._callbacks: Dict[str, Callable[[CallbackCall], None]] = {'display_page': self._displayPageCallback,
                                                                      'push_page': self._pushPageCallback,
                                                                      'pop_page': self._popPageCallback}
        self._page_stack: List[str] = []

        self._streamdecks = DeviceManager().enumerate()
        self._nb_of_streamdecks: int = len(self._streamdecks)

        if self._nb_of_streamdecks == 0:
            raise RuntimeError('StreamDeckLayoutManager: Couldn\'t find any streamdecks.')

        if deck_index >= self._nb_of_streamdecks:
            raise RuntimeError('StreamDeckLayoutManager: Ouf of bounds deck_index.')

        self._deck = self._streamdecks[deck_index]
        if not self._deck.is_visual():
            raise RuntimeError('StreamDeckLayoutManager: StreamDeck does not have any screene.')

        self._deck.open()
        self._deck.reset()

        self._number_of_keys = self._deck.key_count()

        self._initConfig(config_file_path)

        # -- Register callback function for when a key state changes.
        self._deck.set_key_callback(self._keyChangeCallback)

    def _initConfig(self, config_file_path: str) -> None:
        if not os.path.exists(config_file_path):
            raise RuntimeError(f'StreamDeckLayoutManager: Can\'t read config file at \'{config_file_path}\'.')

        data: Optional[Dict[str, Any]] = None

        try:
            with open(config_file_path, mode="rb") as fp:
                data = tomllib.load(fp)

            if data is None:
                raise RuntimeError

        except Exception as e:
            raise RuntimeError(f'StreamDeckLayoutManager: Can\'t read config file at \'{config_file_path}\' ({e}).')

        for config_section, value in data.items():
            if config_section == 'config':
                folder_path = value.get('AssetFolder')
                if folder_path is None:
                    raise RuntimeError(f'StreamDeckLayoutManager: Missing \'AssetFolder\' in \'{config_file_path}\'.')

                self._assets_folder = folder_path if folder_path.startswith('/') else os.path.join(os.path.join(Path(config_file_path).parent, folder_path))

                font_file = value.get('Font')
                if font_file is None:
                    raise RuntimeError(f'StreamDeckLayoutManager: Missing \'Font\' in \'{config_file_path}\'.')

                font_size = value.get('FontSize')
                if font_size is None:
                    raise RuntimeError(f'StreamDeckLayoutManager: Missing \'FontSize\' in \'{config_file_path}\'.')

                self._font = ImageFont.truetype(os.path.join(self._assets_folder, font_file), font_size)

                brightness = value.get('Brightness')
                if brightness is not None:
                    self.setBrightness(brightness)
            else:
                for i in range(self._number_of_keys):
                    key_name = f'Key{i}'

                    config_name = key_name + 'Image'
                    image_name = value.get(config_name)

                    config_name = key_name + 'Label'
                    label = value.get(config_name)

                    if image_name is None and label is None:
                        continue

                    page_and_key_name = f'{config_section}_{key_name}'
                    if self._key_configs.get(page_and_key_name) is not None:
                        raise RuntimeError(f'StreamDeckLayoutManager: Found multiple configurations for page \'{config_section}\' and key \'{i}\'.')


                        print(config_name)
                    if label is not None:
                        print(config_name)

                    config_name = key_name + 'ImageMargins'
                    margins = value.get(config_name)
                    if image_name is not None:
                        print(config_name)

                    config_name = key_name + 'PressedAction'
                    pressed_action = value.get(config_name)
                    if pressed_action is not None:
                        print(config_name)

                    config_name = key_name + 'ReleasedAction'
                    released_action = value.get(config_name)
                    if released_action is not None:
                        print(config_name)

        if self._assets_folder is None:
            raise RuntimeError(f'StreamDeckLayoutManager: Missing \'config\' section in \'{config_file_path}\'.')

    # -- Generates a custom tile with run-time generated text and custom image via the PIL module.
    def _renderKeyImage(self, image_filename: str, label: str) -> Optional[Image.Image]:
        # Resize the source image asset to best-fit the dimensions of a single key,
        # leaving a margin at the bottom so that we can draw the key title
        # afterwards.
        icon = Image.open(image_filename)
        image: Image.Image = PILHelper.create_scaled_image(self._deck, icon, margins=[0, 0, 20, 0])

        # Load a custom TrueType font and use it to overlay the key index, draw key
        # label onto the image a few pixels from the bottom of the key.
        draw = ImageDraw.Draw(image)
        draw.text((image.width / 2, image.height - 5), text=label, font=self._font, anchor='ms', fill='white')

        image = PILHelper.to_native_format(self._deck, image)
        return image

    def _setKeyImage(self, key_index: int, image_file: Optional[str], label: Optional[str]) -> None:
        image: Optional[Image.Image] = None

        if image_file is not None and label is not None and self._assets_folder is not None:
            image_filename = image_file if image_file.startswith('/') else os.path.join(self._assets_folder, image_file)
            # Generate the custom key with the requested image and label.
            image = self._renderKeyImage(image_filename, label)
            if image is None:
                return

        # -- Use a scoped-with on the deck to ensure we're the only thread using it right now.
        with self._deck:
            # -- Update requested key with the generated image.
            self._deck.set_key_image(key_index, image)

    # -- Associated actions when a key is pressed.
    def _keyChangeCallback(self, deck: StreamDeck, key_index: int, state: bool) -> None:
        if self._deck is None or len(self._page_stack) == 0 or self._config is None or deck != self._deck:
            return

        current_page_name = self._page_stack[-1]
        current_page_config = self._config.get(current_page_name)
        if current_page_config is None:
            return

        key_name = f'Key{key_index}'
        action: Optional[List[Any] | CallbackCall] = None

        if state is True:
            action = current_page_config.get(key_name + 'PressedAction')
        else:
            action = current_page_config.get(key_name + 'ReleasedAction')

        if action is None:
            return

        callback_call: Optional[CallbackCall] = None
        if isinstance(action, CallbackCall):
            callback_call = action
        else:
            if not isinstance(action[0], str):
                raise RuntimeError(f'Invalid key action name for key \'{key_name}\'.')

            callback_call = CallbackCall(action)

        callback = self._callbacks.get(callback_call.name())
        if callback is None:
            raise RuntimeError(f'StreamDeckLayoutManager: Unknown callback \'{callback_call.name()}\'.')

        callback(callback_call)

    def _updatePage(self, page_name: str) -> None:
        if self._config is None:
            raise RuntimeError(f'StreamDeckLayoutManager: Missing config for page \'{page_name}\'.')

        page_config = self._config.get(page_name)
        if page_config is None:
            raise RuntimeError(f'StreamDeckLayoutManager: Missing config for page \'{page_name}\'.')

        for key_index in range(self._number_of_keys):
            key_name = f'Key{key_index}'

            image_file = page_config.get(key_name + 'Image')
            label = page_config.get(key_name + 'Label')

            if image_file is not None and label is None:
                image_file = None

            self._setKeyImage(key_index, image_file, label)

    def _displayPageCallback(self, call: CallbackCall) -> None:
        if self._deck is None:
            return

        if call.numberOfArguments() != 1:
            raise RuntimeError('StreamDeckLayoutManager: Invalid arguments to display_page action.')

        self.displayPage(call.argumentAsString(at_index=0))

    def _pushPageCallback(self, call: CallbackCall) -> None:
        if call.numberOfArguments() != 1:
            raise RuntimeError('StreamDeckLayoutManager: Invalid arguments to push_page action.')

        current_page_index = len(self._page_stack) - 1
        if current_page_index < 0:
            raise RuntimeError('StreamDeckLayoutManager: No current page set before calling pushPage().')

        self.pushPage(call.argumentAsString(at_index=0))

    def _popPageCallback(self, call: CallbackCall) -> None:
        if self._deck is None:
            return

        if call.numberOfArguments() != 0:
            raise RuntimeError('StreamDeckLayoutManager: Invalid arguments to pop_page action.')

        current_page_index = len(self._page_stack) - 1
        if current_page_index < 1:
            raise RuntimeError('StreamDeckLayoutManager: No page to pop when calling popPage().')

        self.popPage()

    def setBrightness(self, percentage: int) -> None:
        if self._deck is None:
            return

        self._deck.set_brightness(percentage)

    def displayPage(self, name: str) -> None:
        current_page_index = len(self._page_stack) - 1
        if current_page_index < 0:
            self._page_stack.append(name)
            current_page_index = 0
        else:
            self._page_stack[current_page_index] = name

        self._updatePage(name)

    def pushPage(self, name: str) -> None:
        if self._deck is None:
            return

        self._page_stack.append(name)
        self._updatePage(name)

    def popPage(self) -> None:
        if self._deck is None:
            return

        if len(self._page_stack) == 1:
            return

        self._page_stack = self._page_stack[:-1]
        self._updatePage(self._page_stack[-1])

    def setKey(self, page_name: str, key_index: int, image_file: Optional[str], label: Optional[str], pressed_callback: Optional[CallbackCall], released_callback: Optional[CallbackCall] = None) -> None:
        if self._deck is None or self._config is None:
            return

        page_config = self._config.get(page_name)
        if page_config is None:
            return

        key_name = f'Key{key_index}'
        parameter = key_name + 'Image'
        if image_file is None:
            if parameter in page_config:
                page_config.pop(parameter)
        else:
            page_config[parameter] = image_file

        parameter = key_name + 'Label'
        if label is None:
            if parameter in page_config:
                page_config.pop(parameter)
        else:
            page_config[parameter] = label

        parameter = key_name + 'PressedAction'
        if pressed_callback is None:
            if parameter in page_config:
                page_config.pop(parameter)
        else:
            page_config[parameter] = pressed_callback

        parameter = key_name + 'ReleasedAction'
        if released_callback is None:
            if parameter in page_config:
                page_config.pop(parameter)
        else:
            page_config[parameter] = released_callback

        # -- If we are currently displaying this page then we update the button too
        if len(self._page_stack) > 0 and page_name == self._page_stack[-1]:
            self._setKeyImage(key_index, image_file, label)

    def setCallback(self, callback_name: str, callback: Optional[Callable[[CallbackCall], None]]) -> None:
        if self._deck is None:
            return

        if callback_name in ['display_page', 'push_page', 'pop_page']:
            raise RuntimeError(f'StreamDeckLayoutManager: Callback name \'{callback_name}\' is reserved.')

        if callback is None:
            self._callbacks.pop(callback_name)
        else:
            self._callbacks[callback_name] = callback

    def hasCallbackFor(self, callback_name: str) -> bool:
        return self._callbacks.get(callback_name) is not None

    def shutdown(self) -> None:
        if self._deck is None:
            return

        # -- Use a scoped-with on the deck to ensure we're the only thread using it right now.
        with self._deck:
            # -- Reset deck, clearing all button images.
            self._deck.reset()

            # -- Close deck handle, terminating internal worker threads.
            self._deck.close()

        self._deck = None

    # -- Return the number of stream decks found.
    def numberOfStreamDecks(self) -> int:
        return self._nb_of_streamdecks

    # -- Prints diagnostic information about a given StreamDeck.
    def printDeckInfo(self, index: int) -> None:
        if index >= self._nb_of_streamdecks:
            raise RuntimeError('Out of bounds index for printDeckInof().')

        deck = self._streamdecks[index]
        image_format = deck.key_image_format()

        flip_description: Dict[Tuple[bool, bool], str] = {
            (False, False): 'not mirrored',
            (True, False): 'mirrored horizontally',
            (False, True): 'mirrored vertically',
            (True, True): 'mirrored horizontally/vertically',
        }

        print('Deck {} - {}.'.format(index, deck.deck_type()))
        print('\t - ID: {}'.format(deck.id()))
        print('\t - Serial: \'{}\''.format(deck.get_serial_number()))
        print('\t - Firmware Version: \'{}\''.format(deck.get_firmware_version()))
        print('\t - Key Count: {} (in a {}x{} grid)'.format(
            deck.key_count(),
            deck.key_layout()[0],
            deck.key_layout()[1]))
        if deck.is_visual():
            print('\t - Key Images: {}x{} pixels, {} format, rotated {} degrees, {}'.format(
                image_format['size'][0],
                image_format['size'][1],
                image_format['format'],
                image_format['rotation'],
                flip_description[image_format['flip']]))
        else:
            print('\t - No Visual Output')
