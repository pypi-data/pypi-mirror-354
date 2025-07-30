import requests
import json
import logging

from typing import Tuple, Iterable

logger = logging.getLogger(__name__)

class AnkiManager:
    def __init__(self, address='http://localhost:8765'):
        self.address = address

    def _invoke(self, action, **params):
        request_json = json.dumps({'action': action, 'params': params, 'version': 6})
        response = requests.post(self.address, data=request_json)
        return response.json()

    def create_collection(self, collection_name):
        return self._invoke('createCollection', collection=collection_name)

    def delete_collection(self, collection_name):
        return self._invoke('deleteCollection', collections=[collection_name])

    def get_collection_names(self):
        return self._invoke('collectionNames')['result']

    def add_note(self, anki_collection_name, front, back, model_name="Basic"):
        note = {
            "collectionName": anki_collection_name,
            "modelName": model_name,
            "fields": {
                "Front": front,
                "Back": back
            },
            "options": {"allowDuplicate": False},
            "tags": []
        }
        return self._invoke('addNote', note=note)

    def add_notes(self, anki_collection_name, new_cards: Iterable['Card'], section_names):
        notes_to_add = [{
            "collectionName": anki_collection_name,
            "modelName": "Basic",
            "fields": {
                "Front": card.generate_front(),
                "Back": card.generate_back(section_names)
            },
            "options": {"allowDuplicate": False},
            "tags": []
        } for card in new_cards]
        res = self._invoke('addNotes', notes=notes_to_add)
        # TODO: Warning: Notes already exist in other collection, not adding here.
        if res['error'] is not None:
            if 'cannot create note because it is a duplicate' in res['error']:
                logger.error('Unable to sync with Ankiconnect because the anki collection that is currently open in the desktop app already contains the same cards from a different collection. Anki does not allow duplicate card frontsides, so users must use the same collection name for each anki collection.')
            raise RuntimeError(f"All anki add_notes errors: {res['error']}")
        return res['result'] if isinstance(res['result'], list) else [res['result']]

    def find_notes(self, query):
        return self._invoke('findNotes', query=query)['result']

    def get_notes_info(self, note_ids):
        return self._invoke('notesInfo', notes=note_ids)['result']

    def update_note(self, note_id, card, section_names):
        note = {"id": note_id, "fields": {"Front": card.generate_front(), "Back": card.generate_back(section_names)}}
        return self._invoke('updateNoteFields', note=note)

    def delete_notes(self, note_ids):
        return self._invoke('deleteNotes', notes=note_ids)

    def sync(self):
        return self._invoke('sync')

    def get_notes_for_anki_collection(self, anki_collection_name):
        note_ids = self.find_notes(f'"collection:{anki_collection_name}"')
        return self.get_notes_info(note_ids)

    def sync_collection(self, source_name, cards, section_names, overwrite = False):
        existing_notes = self.get_notes_for_anki_collection(source_name)
        if not existing_notes and source_name not in self.get_collection_names():
            self.create_collection(source_name)
        existing_anki_ids = {note['noteId'] for note in existing_notes}
        if overwrite:
            deleted_notes = self.delete_notes(list(existing_anki_ids))
        cards_to_update = [card for card in cards if card.anki_id and card.anki_id in existing_anki_ids]
        new_cards = [card for card in cards if not card.anki_id or card.anki_id not in existing_anki_ids]
        if cards_to_update:
            for card in cards_to_update:
                self.update_note(card.anki_id, card, section_names)
        if new_cards:
            anki_ids = self.add_notes(source_name, new_cards, section_names)
            for card, anki_id in zip(cards, anki_ids):
                if anki_id and anki_id != 'error':
                    card.anki_id = anki_id

    # TODO
    # def sync_images(self, images_path: Path):
    #     def send_request(action, **params):
    #         response = requests.post('http://localhost:8765', json={"action": action, "version": 6, "params": params})
    #         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
    #         return response.json()
    #     anki_media_root = send_request('getMediaDirPath')['result']
    #     anki_media_files = set(os.listdir(anki_media_root))
    #     collection_images = set(os.listdir(images_path))
    #     for img in anki_media_files-collection_images:
    #         os.remove(Path(anki_media_root, img))
    #     for img in collection_images-anki_media_files:
    #         shutil.copy(Path(images_path, img), anki_media_root)
