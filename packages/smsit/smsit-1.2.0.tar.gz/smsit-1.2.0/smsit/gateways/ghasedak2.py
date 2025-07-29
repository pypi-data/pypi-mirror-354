from requests import post
from requests.exceptions import RequestException

from smsit import Gateway, GatewayError
from smsit.logging import log


class Ghasedak2Gateway(Gateway):
    """
    Ghasedak

    Documentation: https://ghasedak.me/docs

    """

    _gateway_name = "ghasedak2"
    _config_params = ("apikey", "sender")
    _server_url = "https://gateway.ghasedak.me/rest/api/v1"

    _status_map = {
        200: "Success",
        400: "InvalidInput|EmptyReceiver|MissedLaghv11",
        401: "InactiveAccount|NotAuthorized",
        402: "OperationFailed",
        406: "LineOwnershipError",
        412: (
            "InaccessibleLine|InactiveLine|PublicLine|BadOperator|"
            "InvalidProvider|BadService|SelfReceiverLimit|ExpiredLine|"
            "MissedMessageId|UpgradePlan"
        ),
        416: "ForbiddenIp",
        418: "NotEnoughCredit",
        419: "BadTariff",
        420: "MessageInvalidLink",
        422: "MessageInvalidCharacter",
        426: "UpgradePlan",
        428: "InvalidMessageTemplate",
        429: "MissedParams",
        451: "DuplicateRequest",
        413: "MessageLengthLimit|ReceiversMaxLimit",
        500: "UnknownError",
    }

    @staticmethod
    def _normalize_response_keys(v: dict):
        # ghasedak's api just wrote by some drunk monkeys
        return {k.lower(): v for k, v in v.items()}

    def _call(self, path, headers, params):
        try:
            resp = post(
                self._server_url + path,
                headers=headers,
                json=params,
            )
            body = resp.json()
            body = self._normalize_response_keys(body)
            code = int(body["statuscode"])
            if code != 200:
                reason = "%s-%s-%s" % (
                    code,
                    body["message"],
                    self._status_map.get(code),
                )
                raise GatewayError(reason)

        except RequestException:
            log.exception("GatewayError:RequestError")
            raise GatewayError("Cannot send message")

        except Exception:
            log.exception("GatewayError:BadGateway")
            raise GatewayError("Bad gateway")

        return resp

    def send(self, message):
        headers = {
            "apikey": self.config["apikey"],
            "accept": "application/json",
            "cache-control": "no-cache",
        }
        params = {}

        if isinstance(message.meta, dict):
            params.update(message.meta)

        if message.type in ("sms", "voiceMessage"):
            params["message"] = message.text
            params["receptors"] = tuple(map(str, message.receiver))

            if message.type == "voiceMessage":
                params["isVoice"] = True

            sender = message.sender or self.config.get("sender")
            if sender:
                params["lineNumber"] = sender
            return [self._call("/WebService/SendBulkSMS", headers, params)]

        if message.type == "templatedMessage":
            params["templateName"] = message.template
            params["receptors"] = [dict(mobile=x) for x in message.receiver]

            # use new key-value method
            if isinstance(message.params, dict):
                params["inputs"] = []
                for k, v in message.params.items():
                    params["inputs"].append(dict(param=k, value=v))

                return [self._call("/WebService/SendOtpSMS", headers, params)]

            # use classic method (param1,param2,...)
            for k, v in enumerate(message.params):
                params["param%s" % (k + 1)] = v

            return [
                self._call("/WebService/SendOtpWithParams", headers, params)
            ]
