from datetime import datetime
from typing import Any

import requests
from .jalali_to_gregorian import jconvert


class Form:
    BASE_URL = "https://survey.porsline.ir"

    def __init__(self, form_id: int, name: str, api_key: str):
        self.id = form_id
        self.name = name
        self.api_key = api_key
        self.headers = {
            "Authorization": f"API-Key {api_key}",
            "Content-Type": "application/json"
        }
        self._cols = None

    @property
    def cols(self):
        if self._cols is None:
            response = requests.get(f"{self.BASE_URL}/api/v2/surveys/{self.id}/", headers=self.headers)
            response.raise_for_status()
            all_questions = response.json().get("questions", [])
            questions = []
            for q in all_questions:
                questions.append({
                    "id": q["id"],
                    "text": q["title"],
                    "type": q["type"],
                    "options": [{"id": ch["id"], "name": ch["name"]} for ch in q.get("choices", [])]
                })
            self._cols = questions
        return self._cols

    def responses(self, since: str = None, header: bool = False) -> list[dict] | list[list]:
        url = f"{self.BASE_URL}/api/v2/surveys/{self.id}/responses/results-table/?page_size=1000"
        if since:
            url += f"&since={since}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        if header:
            response = response.json()
            body = response["body"]
            header = [
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "choices": item.get("choices") or None,
                    "multiple": item.get("allow_multiple_select") or False
                }
                for item in response["header"]
            ]
            # return body
            refined_body = []
            body_i = 0
            for i, item in enumerate(header):
                step = 1
                if item["multiple"]:
                    refined_body.append([bx.get("data")[body_i: body_i + len(item["choices"])] for bx in body])
                    step = len(item["choices"])
                else:
                    refined_body.append([bx.get("data")[body_i] for bx in body])

                body_i += step

            return [
                [{"head": header[i], "val": refined_body[i][j]} for i in range(len(header))]
                for j in range(len(refined_body[0]))
            ]

        else:
            return [{
                "response": item["data"][2:-2],
                "submitted_at": jconvert(item["data"][-1])}
                for item in response.json()["body"]]
