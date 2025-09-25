"""
Wake E-commerce API Types
Type definitions for Wake API entities
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TipoPessoa(str, Enum):
    FISICA = "Fisica"
    JURIDICA = "Juridica"


class TipoSexo(str, Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"
    NAO_INFORMADO = "NaoInformado"


class Usuario:
    """Wake E-commerce User type definition"""
    
    def __init__(self, data: Dict[str, Any]):
        self.usuarioId: int = data.get("usuarioId")
        self.bloqueado: bool = data.get("bloqueado", False)
        self.grupoInformacaoCadastral: List[Any] = data.get("grupoInformacaoCadastral", [])
        self.tipoPessoa: str = data.get("tipoPessoa")
        self.origemContato: int = data.get("origemContato", 0)
        self.tipoSexo: Optional[str] = data.get("tipoSexo")
        self.nome: str = data.get("nome")
        self.cpf: Optional[str] = data.get("cpf")
        self.email: str = data.get("email")
        self.rg: Optional[str] = data.get("rg")
        self.telefoneResidencial: Optional[str] = data.get("telefoneResidencial")
        self.telefoneCelular: Optional[str] = data.get("telefoneCelular")
        self.telefoneComercial: Optional[str] = data.get("telefoneComercial")
        self.dataNascimento: Optional[str] = data.get("dataNascimento")
        self.razaoSocial: Optional[str] = data.get("razaoSocial")
        self.cnpj: Optional[str] = data.get("cnpj")
        self.inscricaoEstadual: Optional[str] = data.get("inscricaoEstadual")
        self.responsavel: Optional[str] = data.get("responsavel")
        self.dataCriacao: str = data.get("dataCriacao")
        self.dataAtualizacao: Optional[str] = data.get("dataAtualizacao")
        self.revendedor: bool = data.get("revendedor", False)
        self.listaInformacaoCadastral: Optional[List[Any]] = data.get("listaInformacaoCadastral")
        self.avatar: Optional[str] = data.get("avatar")
        self.ip: Optional[str] = data.get("ip")
        self.aprovado: bool = data.get("aprovado", True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Usuario instance back to dictionary"""
        return {
            "usuarioId": self.usuarioId,
            "bloqueado": self.bloqueado,
            "grupoInformacaoCadastral": self.grupoInformacaoCadastral,
            "tipoPessoa": self.tipoPessoa,
            "origemContato": self.origemContato,
            "tipoSexo": self.tipoSexo,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "rg": self.rg,
            "telefoneResidencial": self.telefoneResidencial,
            "telefoneCelular": self.telefoneCelular,
            "telefoneComercial": self.telefoneComercial,
            "dataNascimento": self.dataNascimento,
            "razaoSocial": self.razaoSocial,
            "cnpj": self.cnpj,
            "inscricaoEstadual": self.inscricaoEstadual,
            "responsavel": self.responsavel,
            "dataCriacao": self.dataCriacao,
            "dataAtualizacao": self.dataAtualizacao,
            "revendedor": self.revendedor,
            "listaInformacaoCadastral": self.listaInformacaoCadastral,
            "avatar": self.avatar,
            "ip": self.ip,
            "aprovado": self.aprovado
        }