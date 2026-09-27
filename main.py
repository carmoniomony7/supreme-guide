import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.metrics import dp


class MeuCarroApp(App):

    def build(self):

        self.title = "MEU CARRO"

        # =========================
        # ARQUIVO DOS DADOS
        # =========================

        self.arquivo_dados = os.path.join(
            self.user_data_dir,
            "meu_carro_dados.json"
        )

        self.historico = []

        self.dados_meta = {
            "preco": "",
            "guardado": "",
            "mensal": ""
        }

        self.poupanca_registrada = False

        self.carregar_dados()

        # =========================
        # TELA
        # =========================

        scroll = ScrollView()

        principal = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None
        )

        principal.bind(
            minimum_height=principal.setter("height")
        )

        # =========================
        # TÍTULO
        # =========================

        principal.add_widget(
            Label(
                text="MEU CARRO",
                font_size=dp(32),
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        # =========================
        # SALÁRIO
        # =========================

        principal.add_widget(
            Label(
                text="Digite o seu salário (MT):",
                font_size=dp(20),
                size_hint_y=None,
                height=dp(40)
            )
        )

        self.salario = TextInput(
            hint_text="Ex: 36000",
            input_filter="float",
            multiline=False,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50)
        )

        principal.add_widget(self.salario)

        # =========================
        # DISTRIBUIÇÃO
        # =========================

        principal.add_widget(
            Label(
                text="DISTRIBUIÇÃO DO SALÁRIO",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(50)
            )
        )

        self.distribuicao = Label(
            text="Digite o salário e clique em CALCULAR.",
            font_size=dp(18),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(180)
        )

        self.distribuicao.bind(
            size=self.distribuicao.setter("text_size")
        )

        principal.add_widget(self.distribuicao)

        # =========================
        # CALCULAR
        # =========================

        calcular = Button(
            text="CALCULAR",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(55)
        )

        calcular.bind(
            on_press=self.calcular_salario
        )

        principal.add_widget(calcular)

        # =========================
        # REGISTRO DE GASTOS
        # =========================

        principal.add_widget(
            Label(
                text="REGISTRO DE GASTOS",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(50)
            )
        )

        self.alimentacao = self.criar_campo(
            principal,
            "Quanto gastou em alimentação?"
        )

        self.higiene = self.criar_campo(
            principal,
            "Quanto gastou em higiene?"
        )

        self.casa = self.criar_campo(
            principal,
            "Quanto gastou em casa?"
        )

        self.transporte = self.criar_campo(
            principal,
            "Quanto gastou em transporte?"
        )

        self.poupanca = self.criar_campo(
            principal,
            "Quanto guardou para o carro?"
        )

        self.emergencia = self.criar_campo(
            principal,
            "Quanto gastou em emergência?"
        )

        # =========================
        # REGISTRAR GASTOS
        # =========================

        registrar = Button(
            text="REGISTRAR GASTOS",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60)
        )

        registrar.bind(
            on_press=self.registrar_gastos
        )

        principal.add_widget(registrar)

        # =========================
        # NOVO MÊS
        # =========================

        novo_mes = Button(
            text="NOVO MÊS",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60)
        )

        novo_mes.bind(
            on_press=self.novo_mes
        )

        principal.add_widget(novo_mes)

        # =========================
        # RESULTADO
        # =========================

        principal.add_widget(
            Label(
                text="RESULTADO",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(50)
            )
        )

        self.resultado = Label(
            text="",
            font_size=dp(18),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(900)
        )

        self.resultado.bind(
            size=self.resultado.setter("text_size")
        )

        principal.add_widget(self.resultado)

        # =========================
        # HISTÓRICO
        # =========================

        principal.add_widget(
            Label(
                text="HISTÓRICO DOS MESES",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(55)
            )
        )

        self.resultado_historico = Label(
            text="Nenhum mês registrado ainda.",
            font_size=dp(18),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(250)
        )

        self.resultado_historico.bind(
            size=self.resultado_historico.setter(
                "text_size"
            )
        )

        principal.add_widget(
            self.resultado_historico
        )

        # =========================
        # APAGAR HISTÓRICO
        # =========================

        apagar = Button(
            text="APAGAR HISTÓRICO",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60)
        )

        apagar.bind(
            on_press=self.confirmar_apagar_historico
        )

        principal.add_widget(apagar)

        # =========================
        # META DO CARRO
        # =========================

        principal.add_widget(
            Label(
                text="META DO CARRO",
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(50)
            )
        )

        self.preco_carro = self.criar_campo(
            principal,
            "Quanto custa o carro?"
        )

        self.guardado = self.criar_campo(
            principal,
            "Quanto já tem guardado?"
        )

        self.meta_mensal = self.criar_campo(
            principal,
            "Quanto pretende guardar por mês?"
        )

        # =========================
        # CALCULAR META
        # =========================

        meta = Button(
            text="CALCULAR META",
            font_size=dp(20),
            size_hint_y=None,
            height=dp(60)
        )

        meta.bind(
            on_press=self.calcular_meta
        )

        principal.add_widget(meta)

        # =========================
        # RESULTADO DA META
        # =========================

        self.resultado_meta = Label(
            text="",
            font_size=dp(19),
            halign="left",
            valign="top",
            size_hint_y=None,
            height=dp(300)
        )

        self.resultado_meta.bind(
            size=self.resultado_meta.setter("text_size")
        )

        principal.add_widget(self.resultado_meta)

        principal.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(30)
            )
        )

        scroll.add_widget(principal)

        # =========================
        # RECUPERAR META
        # =========================

        self.preco_carro.text = str(
            self.dados_meta.get("preco", "")
        )

        self.guardado.text = str(
            self.dados_meta.get("guardado", "")
        )

        self.meta_mensal.text = str(
            self.dados_meta.get("mensal", "")
        )

        self.atualizar_historico()

        return scroll

    # ==================================================
    # CRIAR CAMPO
    # ==================================================

    def criar_campo(self, layout, texto):

        layout.add_widget(
            Label(
                text=texto,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(40)
            )
        )

        campo = TextInput(
            hint_text="Digite o valor",
            input_filter="float",
            multiline=False,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(50)
        )

        layout.add_widget(campo)

        return campo

    # ==================================================
    # CARREGAR DADOS
    # ==================================================

    def carregar_dados(self):

        if not os.path.exists(
            self.arquivo_dados
        ):
            return

        try:

            with open(
                self.arquivo_dados,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

            self.historico = dados.get(
                "historico",
                []
            )

            self.dados_meta = dados.get(
                "meta",
                {
                    "preco": "",
                    "guardado": "",
                    "mensal": ""
                }
            )

            self.poupanca_registrada = dados.get(
                "poupanca_registrada",
                False
            )

        except:

            self.historico = []

            self.dados_meta = {
                "preco": "",
                "guardado": "",
                "mensal": ""
            }

            self.poupanca_registrada = False

    # ==================================================
    # SALVAR DADOS
    # ==================================================

    def salvar_dados(self):

        dados = {

            "historico": self.historico,

            "meta": {
                "preco": self.preco_carro.text,
                "guardado": self.guardado.text,
                "mensal": self.meta_mensal.text
            },

            "poupanca_registrada":
                self.poupanca_registrada
        }

        try:

            with open(
                self.arquivo_dados,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    dados,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as erro:

            print(
                "Erro ao salvar:",
                erro
            )

    # ==================================================
    # CALCULAR SALÁRIO
    # ==================================================

    def calcular_salario(self, instance):

        try:

            salario = float(
                self.salario.text
            )

            alimentacao = salario * 0.30
            higiene = salario * 0.10
            casa = salario * 0.20
            transporte = salario * 0.10
            poupanca = salario * 0.20
            emergencia = salario * 0.10

            self.orcamentos = {

                "Alimentação": alimentacao,
                "Higiene": higiene,
                "Casa": casa,
                "Transporte": transporte,
                "Poupança": poupanca,
                "Emergência": emergencia
            }

            self.distribuicao.text = (

                f"Alimentação: "
                f"{alimentacao:.2f} MT\n"

                f"Higiene: "
                f"{higiene:.2f} MT\n"

                f"Casa: "
                f"{casa:.2f} MT\n"

                f"Transporte: "
                f"{transporte:.2f} MT\n"

                f"Poupança: "
                f"{poupanca:.2f} MT\n"

                f"Emergência: "
                f"{emergencia:.2f} MT\n\n"

                f"Total: "
                f"{salario:.2f} MT"
            )

        except:

            self.distribuicao.text = (
                "Digite um salário válido."
            )

    # ==================================================
    # REGISTRAR GASTOS
    # ==================================================

    def registrar_gastos(self, instance):

        if not hasattr(
            self,
            "orcamentos"
        ):

            self.resultado.text = (
                "Primeiro digite o salário "
                "e clique em CALCULAR."
            )

            return

        try:

            alimentacao = float(
                self.alimentacao.text or 0
            )

            higiene = float(
                self.higiene.text or 0
            )

            casa = float(
                self.casa.text or 0
            )

            transporte = float(
                self.transporte.text or 0
            )

            poupanca = float(
                self.poupanca.text or 0
            )

            emergencia = float(
                self.emergencia.text or 0
            )

            # =========================
            # DESPESAS
            # =========================

            despesas = {

                "Alimentação": alimentacao,
                "Higiene": higiene,
                "Casa": casa,
                "Transporte": transporte,
                "Emergência": emergencia
            }

            texto = ""
            total_despesas = 0

            # =========================
            # VERIFICAR CATEGORIAS
            # =========================

            for categoria, gasto in despesas.items():

                orcamento = self.orcamentos[
                    categoria
                ]

                restante = (
                    orcamento - gasto
                )

                total_despesas += gasto

                texto += (
                    f"{categoria}\n"
                    f"Orçamento: "
                    f"{orcamento:.2f} MT\n"
                    f"Gasto: "
                    f"{gasto:.2f} MT\n"
                    f"Restante: "
                    f"{restante:.2f} MT\n"
                )

                if restante < 0:

                    ultrapassou = abs(
                        restante
                    )

                    texto += (
                        f"⚠️ ULTRAPASSOU "
                        f"EM: {ultrapassou:.2f} MT\n\n"
                    )

                elif restante == 0:

                    texto += (
                        "⚠️ O ORÇAMENTO ACABOU.\n\n"
                    )

                else:

                    texto += (
                        f"✅ DISPONÍVEL: "
                        f"{restante:.2f} MT\n\n"
                    )

            # =========================
            # SALÁRIO
            # =========================

            salario = float(
                self.salario.text
            )

            # =========================
            # SALDO LIVRE
            # =========================
            #
            # Salário - despesas - poupança
            #

            saldo_livre = (
                salario
                - total_despesas
                - poupanca
            )

            # =========================
            # POUPANÇA → META
            # =========================

            mensagem_poupanca = ""

            if not self.poupanca_registrada:

                guardado_atual = float(
                    self.guardado.text or 0
                )

                novo_guardado = (
                    guardado_atual
                    + poupanca
                )

                self.guardado.text = (
                    f"{novo_guardado:.2f}"
                )

                self.poupanca_registrada = True

                mensagem_poupanca = (

                    "\nPOUPANÇA PARA O CARRO\n"
                    "====================\n"

                    f"Este mês: "
                    f"{poupanca:.2f} MT\n"

                    f"Total guardado: "
                    f"{novo_guardado:.2f} MT\n"
                )

            else:

                mensagem_poupanca = (

                    "\nPOUPANÇA PARA O CARRO\n"
                    "====================\n"

                    f"{poupanca:.2f} MT "
                    "já foi registrada neste mês.\n"

                    "Não será adicionada novamente.\n"
                )

            # =========================
            # RESUMO FINANCEIRO
            # =========================

            texto += (

                mensagem_poupanca

                + "\n"
                "RESUMO FINANCEIRO\n"
                "====================\n"

                f"Salário: "
                f"{salario:.2f} MT\n"

                f"Total de despesas: "
                f"{total_despesas:.2f} MT\n"

                f"Poupança: "
                f"{poupanca:.2f} MT\n"
            )

            # =========================
            # SITUAÇÃO DO SALDO LIVRE
            # =========================

            if saldo_livre > 0:

                texto += (
                    f"\n💰 SALDO LIVRE: "
                    f"{saldo_livre:.2f} MT\n"
                    "Este valor ainda está disponível."
                )

            elif saldo_livre == 0:

                texto += (
                    "\n⚠️ SALDO LIVRE: 0.00 MT\n"
                    "Todo o salário foi distribuído."
                )

            else:

                excesso = abs(
                    saldo_livre
                )

                texto += (
                    f"\n⚠️ SALDO NEGATIVO: "
                    f"{saldo_livre:.2f} MT\n"
                    f"Os gastos ultrapassaram "
                    f"o salário em {excesso:.2f} MT."
                )

            self.resultado.text = texto

            # =========================
            # HISTÓRICO
            # =========================

            registro = {

                "salario": salario,

                "total_gastos":
                    total_despesas,

                "poupanca":
                    poupanca,

                "saldo":
                    saldo_livre
            }

            self.historico.append(
                registro
            )

            self.salvar_dados()

            self.atualizar_historico()

            # Atualizar meta
            self.calcular_meta(None)

        except:

            self.resultado.text = (
                "Verifique os valores digitados."
            )

    # ==================================================
    # ATUALIZAR HISTÓRICO
    # ==================================================

    def atualizar_historico(self):

        if not hasattr(
            self,
            "resultado_historico"
        ):
            return

        if not self.historico:

            self.resultado_historico.text = (
                "Nenhum mês registrado ainda."
            )

            return

        texto = ""

        numero = 1

        for registro in self.historico:

            poupanca = float(
                registro.get(
                    "poupanca",
                    0
                )
            )

            saldo = float(
                registro.get(
                    "saldo",
                    0
                )
            )

            texto += (

                f"MÊS {numero}\n"

                f"Salário: "
                f"{float(registro['salario']):.2f} MT\n"

                f"Total de despesas: "
                f"{float(registro['total_gastos']):.2f} MT\n"

                f"Poupança: "
                f"{poupanca:.2f} MT\n"

                f"Saldo livre: "
                f"{saldo:.2f} MT\n\n"
            )

            numero += 1

        self.resultado_historico.text = texto

        linhas = (
            len(self.historico) * 6
            + 2
        )

        self.resultado_historico.height = (
            dp(30 * linhas)
        )

    # ==================================================
    # CONFIRMAR APAGAR HISTÓRICO
    # ==================================================

    def confirmar_apagar_historico(self, instance):

        layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(15)
        )

        mensagem = Label(
            text=(
                "Tem certeza que deseja "
                "apagar todo o histórico?\n\n"
                "Esta ação não pode ser desfeita."
            ),
            font_size=dp(18)
        )

        botoes = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(55)
        )

        cancelar = Button(
            text="CANCELAR",
            font_size=dp(17)
        )

        apagar = Button(
            text="APAGAR",
            font_size=dp(17)
        )

        botoes.add_widget(cancelar)
        botoes.add_widget(apagar)

        layout.add_widget(mensagem)
        layout.add_widget(botoes)

        popup = Popup(
            title="APAGAR HISTÓRICO",
            content=layout,
            size_hint=(0.9, 0.4),
            auto_dismiss=False
        )

        cancelar.bind(
            on_press=popup.dismiss
        )

        apagar.bind(
            on_press=lambda x:
            self.apagar_historico(popup)
        )

        popup.open()

    # ==================================================
    # APAGAR HISTÓRICO
    # ==================================================

    def apagar_historico(self, popup):

        self.historico = []

        self.salvar_dados()

        self.atualizar_historico()

        self.resultado.text = (
            "O histórico foi apagado."
        )

        popup.dismiss()

    # ==================================================
    # NOVO MÊS
    # ==================================================

    def novo_mes(self, instance):

        self.alimentacao.text = ""
        self.higiene.text = ""
        self.casa.text = ""
        self.transporte.text = ""
        self.poupanca.text = ""
        self.emergencia.text = ""

        # Liberar nova poupança
        self.poupanca_registrada = False

        self.salvar_dados()

        self.resultado.text = (

            "NOVO MÊS\n\n"

            "Os gastos foram limpos.\n"

            "A poupança do novo mês "
            "poderá ser adicionada à meta.\n\n"

            "O histórico anterior "
            "continua guardado."
        )

    # ==================================================
    # CALCULAR META
    # ==================================================

    def calcular_meta(self, instance):

        try:

            preco = float(
                self.preco_carro.text
            )

            guardado = float(
                self.guardado.text
            )

            mensal = float(
                self.meta_mensal.text or 0
            )

            falta = (
                preco - guardado
            )

            self.salvar_dados()

            if falta <= 0:

                self.resultado_meta.text = (

                    "META CONCLUÍDA!\n\n"

                    "Já tens dinheiro suficiente "
                    "para atingir o valor da meta."
                )

                return

            if mensal <= 0:

                self.resultado_meta.text = (

                    "OBJETIVO\n\n"

                    f"Preço do carro: "
                    f"{preco:.2f} MT\n"

                    f"Já guardado: "
                    f"{guardado:.2f} MT\n"

                    f"Falta: "
                    f"{falta:.2f} MT\n\n"

                    "Digite quanto pretende "
                    "guardar por mês."
                )

                return

            meses = (
                falta / mensal
            )

            meses_arredondados = int(
                meses
            )

            if meses > meses_arredondados:

                meses_arredondados += 1

            progresso = (
                guardado / preco
            ) * 100

            if progresso > 100:

                progresso = 100

            self.resultado_meta.text = (

                "OBJETIVO\n\n"

                f"Preço do carro: "
                f"{preco:.2f} MT\n"

                f"Já guardado: "
                f"{guardado:.2f} MT\n"

                f"Falta: "
                f"{falta:.2f} MT\n\n"

                f"Tempo estimado: "
                f"{meses_arredondados} meses\n"

                f"Progresso: "
                f"{progresso:.2f}%"
            )

        except:

            self.resultado_meta.text = (
                "Preencha corretamente "
                "os campos da meta."
            )


# ======================================================
# INICIAR
# ======================================================

if __name__ == "__main__":

    MeuCarroApp().run()