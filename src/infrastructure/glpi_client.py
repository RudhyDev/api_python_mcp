"""
Cliente HTTP para a API do GLPI.
"""
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Optional
from src.core.glpi_entities import GLPIConfig, GLPIResponse


class GLPIHTTPClient:
    """Cliente HTTP para fazer requisições à API do GLPI."""

    def __init__(self, config: GLPIConfig):
        self.config = config
        self.session_token = None

    def authenticate(self) -> bool:
        """Autentica na API do GLPI."""
        try:
            headers = {
                "Content-Type": "application/json",
                "App-Token": self.config.app_token,
            }

            # Se tiver user_token, adiciona ao header
            if self.config.user_token:
                headers["Authorization"] = f"user_token {self.config.user_token}"

            req = urllib.request.Request(
                f"{self.config.base_url}/initSession", headers=headers, method="GET"
            )

            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                data = json.loads(response.read().decode())
                self.session_token = data.get("session_token")

                return self.session_token is not None

        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return False

    def make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> GLPIResponse:
        """Faz uma requisição para a API do GLPI."""
        if not self.session_token:
            if not self.authenticate():
                return GLPIResponse(401, {}, "Falha na autenticação")

        url = f"{self.config.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "App-Token": self.config.app_token,
        }
        
        # Adiciona session token se disponível
        if self.session_token:
            headers["Session-Token"] = self.session_token

        try:
            if method == "GET":
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(
                    req, timeout=self.config.timeout
                ) as response:
                    data = json.loads(response.read().decode())
                    return GLPIResponse(response.getcode(), data)

            elif method == "POST":
                json_data = json.dumps(data).encode("utf-8")
                req = urllib.request.Request(
                    url, data=json_data, headers=headers, method="POST"
                )
                with urllib.request.urlopen(
                    req, timeout=self.config.timeout
                ) as response:
                    data = json.loads(response.read().decode())
                    return GLPIResponse(response.getcode(), data)

            elif method == "PUT":
                json_data = json.dumps(data).encode("utf-8")
                req = urllib.request.Request(
                    url, data=json_data, headers=headers, method="PUT"
                )
                with urllib.request.urlopen(
                    req, timeout=self.config.timeout
                ) as response:
                    data = json.loads(response.read().decode())
                    return GLPIResponse(response.getcode(), data)

            elif method == "DELETE":
                req = urllib.request.Request(url, headers=headers, method="DELETE")
                with urllib.request.urlopen(
                    req, timeout=self.config.timeout
                ) as response:
                    data = json.loads(response.read().decode())
                    return GLPIResponse(response.getcode(), data)

        except urllib.error.HTTPError as e:
            error_data = {}
            try:
                error_data = json.loads(e.read().decode())
            except Exception:
                pass
            return GLPIResponse(e.code, error_data, f"Erro HTTP {e.code}: {e.reason}")

        except urllib.error.URLError as e:
            return GLPIResponse(
                0,
                {},
                f"Erro na conexão: {str(e.reason)} - "
                "Verifique se a URL do GLPI está correta e acessível",
            )

        except Exception as e:
            return GLPIResponse(0, {}, f"Erro desconhecido: {str(e)}")
        
        # Fallback se nenhum método corresponder
        return GLPIResponse(405, {}, "Método não suportado")

    def logout(self) -> bool:
        """Encerra sessão na API do GLPI."""
        try:
            if self.session_token:
                response = self.make_request("GET", "/killSession")
                self.session_token = None
                return response.is_success()
            return True
        except Exception as e:
            print(f"Erro ao encerrar sessão: {e}")
            return False
