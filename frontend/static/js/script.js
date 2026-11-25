/* 1. SELECIONANDO ELEMENTOS HTML */

const titulo = document.querySelector(".header h1");

const mensagem = document.querySelector(".header p");

const botaoPrincipal = document.querySelector(".btn-primary");

const botaoSecundario = document.querySelector(".btn-secondary");


/* 2. PRIMEIRA FUNÇÃO */

function exibirMensagem(texto) {

    mensagem.textContent = texto;

}

/* 2.1. SISTEMA DE NOTIFICAÇÕES */

// Selecionando os elementos HTML.
const notificacao = document.querySelector("#notificacao");

const notificacaoIcone = document.querySelector(
    "#notificacao-icone"
);

const notificacaoTitulo = document.querySelector(
    "#notificacao-titulo"
);

const notificacaoMensagem = document.querySelector(
    "#notificacao-mensagem"
);

// Função responsável por exibir notificações.
function exibirNotificacao(titulo, texto, tipo = "sucesso") {

    // Define o título e a mensagem.
    notificacaoTitulo.textContent = titulo;

    notificacaoMensagem.textContent = texto;

    // Define o tipo de notificação.
    notificacao.classList.remove("sucesso", "erro");

    notificacao.classList.add(tipo);

    // Define o ícone.
    notificacaoIcone.textContent = tipo === "sucesso" ? "✓" : "!";

    // Exibe a notificação.
    notificacao.classList.add("ativa");

    // Esconde a notificação após 4 segundos.
    setTimeout(function() {

        notificacao.classList.remove("ativa");

    }, 4000);

}

/* 3. EVENTO DE CLIQUE BOTÃO NOVA MOVIMENTAÇÃO */

botaoPrincipal.addEventListener("click", function() {});


/* 4. EVENTO DE CLIQUE BOTÃO VER TODAS */

botaoSecundario.addEventListener("click", function() {

    exibirMensagem("Aqui você poderá consultar todas as suas movimentações!");

});


/* 5. MENU DE NAVEGAÇÃO */

const linksMenu = document.querySelectorAll(".sidebar nav a");

linksMenu.forEach(function(link) {

    link.addEventListener("click", function(event) {

        event.preventDefault();

        linksMenu.forEach(function(item) {
            item.classList.remove("active");
        });

        link.classList.add("active");

        exibirMensagem("Seção selecionada: " + link.textContent);

    });

});


/* 6. MENSAGEM INICIAL*/

console.log("Simulador de Gastos iniciado com sucesso!");


/* 7. CONECTANDO JAVASCRIPT À API */

// Armazena as movimentações recebidas do Backend.
let movimentacoesCarregadas = [];

// Seleciona os elementos HTML.
const lista = document.querySelector("#lista-movimentacoes");

const elementoSaldo = document.querySelector("#saldo");

const elementoReceitas = document.querySelector("#receitas");

const elementoDespesas = document.querySelector("#despesas");

// Seleciona o resumo da quantidade de movimentações exibidas.
const resumoResultados = document.querySelector("#resumo-resultados");

const campoBusca = document.querySelector("#busca-movimentacoes");

// Seleciona o filtro por tipo de movimentação.
const filtroTipo = document.querySelector(
    "#filtro-tipo-movimentacao"
);

const filtroCategoria = document.querySelector(
    "#filtro-categoria"
);

const campoDataInicial = document.querySelector("#data-inicial");

const campoDataFinal = document.querySelector("#data-final");

// Seleciona o botão para limpar todos os filtros.
const botaoLimparFiltros = document.querySelector(
    "#btn-limpar-filtros"
);


/* CONVERTE DATA BRASILEIRA PARA O FORMATO AAAA-MM-DD */

function converterDataParaISO(dataTexto) {

    if (!dataTexto) {
        return "";
    }

    const partes = dataTexto.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);

    if (!partes) {
        return null;
    }

    const dia = Number(partes[1]);
    const mes = Number(partes[2]);
    const ano = Number(partes[3]);

    if (ano < 1000 || mes < 1 || mes > 12) {
        return null;
    }

    const ultimoDiaDoMes = new Date(ano, mes, 0).getDate();

    if (dia < 1 || dia > ultimoDiaDoMes) {
        return null;
    }

    return `${ano}-${String(mes).padStart(2, "0")}-${String(dia).padStart(2, "0")}`;
}

/* FORMATA AUTOMATICAMENTE AS DATAS */

function formatarDataDigitada(campo) {

    // Remove tudo que não for número.
    const numeros = campo.value.replace(/\D/g, "").slice(0, 8);

    // Formata os números no padrão DD/MM/AAAA.
    if (numeros.length > 4) {

        campo.value =
            numeros.slice(0, 2) + "/" +
            numeros.slice(2, 4) + "/" +
            numeros.slice(4);

    } else if (numeros.length > 2) {

        campo.value =
            numeros.slice(0, 2) + "/" +
            numeros.slice(2);

    } else {

        campo.value = numeros;

    }

}

/* VALIDAR PERÍODO DAS MOVIMENTAÇÕES */

function validarPeriodo() {

    const dataInicial = converterDataParaISO(campoDataInicial.value);

    const dataFinal = converterDataParaISO(campoDataFinal.value);

    campoDataInicial.setCustomValidity("");
    campoDataFinal.setCustomValidity("");

    if (campoDataInicial.value && dataInicial === null) {

        campoDataInicial.setCustomValidity(
            "Digite uma data inicial válida no formato DD/MM/AAAA."
        );

        return false;
    }

    if (campoDataFinal.value && dataFinal === null) {

        campoDataFinal.setCustomValidity(
            "Digite uma data final válida no formato DD/MM/AAAA."
        );

        return false;
    }

    if (dataInicial && dataFinal && dataInicial > dataFinal) {

        campoDataFinal.setCustomValidity(
            "A data final não pode ser anterior à data inicial."
        );

        return false;
    }

    return true;
}

// Formata valores monetários em Real.
function formatarMoeda(valor) {

    return valor.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });

}

/* CARREGAR CATEGORIAS AUTOMATICAMENTE */

function carregarCategorias() {

    // Guarda a categoria atualmente selecionada.
    const categoriaSelecionada = filtroCategoria.value;

    // Identifica todas as categorias existentes.
    const categorias = [
        ...new Set(
            movimentacoesCarregadas.map(function(movimentacao) {
                return movimentacao.categoria.trim();
            })
        )
    ];

    // Organiza as categorias em ordem alfabética.
    categorias.sort(function(a, b) {
        return a.localeCompare(b, "pt-BR");
    });

    // Limpa as opções anteriores.
    filtroCategoria.innerHTML = "";

    // Cria a opção para mostrar todas as categorias.
    const opcaoTodas = document.createElement("option");
    opcaoTodas.value = "todas";
    opcaoTodas.textContent = "Todas as categorias";
    filtroCategoria.appendChild(opcaoTodas);

    // Cria uma opção para cada categoria encontrada.
    categorias.forEach(function(categoria) {
        const opcao = document.createElement("option");

        opcao.value = categoria;
        opcao.textContent = categoria;

        filtroCategoria.appendChild(opcao);
    });

    // Mantém a seleção anterior, se a categoria ainda existir.
    const categoriaAindaExiste = categorias.some(function(categoria) {
        return categoria.toLowerCase() === categoriaSelecionada.toLowerCase();
    });

    if (categoriaAindaExiste) {
        filtroCategoria.value = categoriaSelecionada;
    } else {
        filtroCategoria.value = "todas";
    }
}

// Função responsável por desenhar a tabela.
function renderizarMovimentacoes(movimentacoes) {

    lista.innerHTML = "";

    if (movimentacoes.length === 0) {

        const linha = document.createElement("tr");

        const coluna = document.createElement("td");

        // Faz a mensagem ocupar todas as colunas da tabela.
        coluna.colSpan = 6;

        // Adiciona uma classe para estilização no CSS.
        coluna.classList.add("mensagem-sem-resultados");

        // Define a mensagem conforme a situação.
        coluna.textContent = movimentacoesCarregadas.length === 0
            ? "Nenhuma movimentação cadastrada."
            : "Nenhuma movimentação encontrada. Tente alterar ou limpar os filtros.";

        // Adiciona a mensagem à tabela.
        linha.appendChild(coluna);

        lista.appendChild(linha);

        return;

    }


    movimentacoes.forEach(function(movimentacao) {

        const linha = document.createElement("tr");

        const descricao = document.createElement("td");
        descricao.textContent = movimentacao.descricao;

        const categoria = document.createElement("td");
        categoria.textContent = movimentacao.categoria;

        const data = document.createElement("td");
        data.textContent = new Date(
            movimentacao.data + "T00:00:00"
        ).toLocaleDateString("pt-BR");

        const tipo = document.createElement("td");

        // Cria uma etiqueta para identificar o tipo.
        const etiquetaTipo = document.createElement("span");

        // Define o texto e a classe da etiqueta.
        if (movimentacao.tipo === "entrada") {

            etiquetaTipo.textContent = "Receita";

            etiquetaTipo.classList.add("tipo-entrada");

        } else if (movimentacao.tipo === "saida") {

            etiquetaTipo.textContent = "Despesa";

            etiquetaTipo.classList.add("tipo-saida");

        }

        // Adiciona a etiqueta dentro da coluna.
        tipo.appendChild(etiquetaTipo);

        const valor = document.createElement("td");

        valor.textContent = formatarMoeda(
            Number(movimentacao.valor)
        );

        // Aplica uma cor conforme o tipo de movimentação.
        if (movimentacao.tipo === "entrada") {

            valor.classList.add("valor-entrada");

        } else if (movimentacao.tipo === "saida") {

            valor.classList.add("valor-saida");

        }

        linha.appendChild(descricao);
        linha.appendChild(categoria);
        linha.appendChild(data);
        linha.appendChild(tipo);
        linha.appendChild(valor);


        // Criando a coluna de ações.
        const acoes = document.createElement("td");


        // Criando o botão de editar.
        const botaoEditar = document.createElement("button");

        botaoEditar.textContent = "Editar";
        botaoEditar.classList.add("btn-editar");

        botaoEditar.dataset.id = movimentacao.id;


        // Criando o botão de excluir.
        const botaoExcluir = document.createElement("button");

        botaoExcluir.textContent = "Excluir";
        botaoExcluir.classList.add("btn-excluir");

        botaoExcluir.dataset.id = movimentacao.id;


        // Adicionando os botões à coluna.
        acoes.appendChild(botaoEditar);
        acoes.appendChild(botaoExcluir);

        // Adicionando a coluna à linha.
        linha.appendChild(acoes);

        // Adicionando a linha à tabela.
        lista.appendChild(linha);

    });

}


// Aplica a pesquisa e os filtros.
// Aplica a pesquisa e todos os filtros.
function aplicarPesquisa() {

    // Verifica se existe algum filtro aplicado.
    const existemFiltrosAtivos =
        campoBusca.value.trim() !== "" ||
        filtroTipo.value !== "todos" ||
        filtroCategoria.value !== "todas" ||
        campoDataInicial.value.trim() !== "" ||
        campoDataFinal.value.trim() !== "";

    // Ativa ou desativa o botão conforme os filtros.
    botaoLimparFiltros.disabled = !existemFiltrosAtivos;

    // Verifica se o período escolhido é válido.
    if (!validarPeriodo()) {
        return;
    }

    // Captura os valores dos filtros.
    const termo = campoBusca.value.trim().toLowerCase();

    const tipoSelecionado = filtroTipo.value;

    const categoriaSelecionada = filtroCategoria.value;

    const dataInicial = converterDataParaISO(campoDataInicial.value);

    const dataFinal = converterDataParaISO(campoDataFinal.value);

    // Filtra as movimentações.
    const movimentacoesFiltradas = movimentacoesCarregadas.filter(
        function(movimentacao) {

            // Verifica a descrição.
            const correspondeDescricao = movimentacao.descricao
                .toLowerCase()
                .includes(termo);

            // Verifica o tipo.
            const correspondeTipo = tipoSelecionado === "todos" ||
                movimentacao.tipo === tipoSelecionado;

            // Verifica a categoria.
            const correspondeCategoria = categoriaSelecionada === "todas" ||
                movimentacao.categoria.toLowerCase() ===
                categoriaSelecionada.toLowerCase();

            // Verifica a data inicial.
            const correspondeDataInicial = !dataInicial ||
                movimentacao.data >= dataInicial;

            // Verifica a data final.
            const correspondeDataFinal = !dataFinal ||
                movimentacao.data <= dataFinal;

            // Todos os critérios precisam ser atendidos.
            return correspondeDescricao &&
                correspondeTipo &&
                correspondeCategoria &&
                correspondeDataInicial &&
                correspondeDataFinal;
        }
    );

    // Atualiza a tabela.
    renderizarMovimentacoes(movimentacoesFiltradas);

    // Calcula a quantidade de resultados encontrados.
    const quantidadeResultados = movimentacoesFiltradas.length;

    // Calcula a quantidade total de movimentações cadastradas.
    const quantidadeTotal = movimentacoesCarregadas.length;

    // Define a palavra correta conforme a quantidade de resultados.
    const textoResultados = quantidadeResultados === 1
        ? "movimentação"
        : "movimentações";

    // Define a palavra correta conforme a quantidade total.
    const textoTotal = quantidadeTotal === 1
        ? "movimentação"
        : "movimentações";

    // Atualiza o resumo exibido acima da tabela.
    if (quantidadeResultados === quantidadeTotal) {

        resumoResultados.textContent =
            `Exibindo ${quantidadeResultados} ${textoResultados}`;

    } else {

        resumoResultados.textContent =
            `Exibindo ${quantidadeResultados} ${textoResultados} de ${quantidadeTotal} ${textoTotal}`;

    }

}


// EVENTOS DOS FILTROS.

campoBusca.addEventListener("input", aplicarPesquisa);

filtroTipo.addEventListener("change", aplicarPesquisa);

filtroCategoria.addEventListener("change", aplicarPesquisa);


/* EVENTOS DOS FILTROS DE DATA */

// Evento da data inicial.
campoDataInicial.addEventListener("change", function() {

    if (!validarPeriodo()) {

        // Se a data inicial estiver inválida, mostra o erro nela.
        if (
            campoDataInicial.value &&
            converterDataParaISO(campoDataInicial.value) === null
        ) {
            campoDataInicial.reportValidity();

        } else {

            // Se o problema for o intervalo, mostra o erro na data final.
            campoDataFinal.reportValidity();

        }

        return;
    }

    aplicarPesquisa();

});


// Evento da data final.
campoDataFinal.addEventListener("change", function() {

    if (!validarPeriodo()) {

        campoDataFinal.reportValidity();

        return;
    }

    aplicarPesquisa();

});

/* EVENTO PARA LIMPAR TODOS OS FILTROS */

botaoLimparFiltros.addEventListener("click", function() {

    // Limpa a barra de pesquisa.
    campoBusca.value = "";

    // Reseta o filtro de categoria.
    filtroCategoria.value = "todas";

    // Reseta o filtro de tipo.
    filtroTipo.value = "todos";

    // Limpa a data inicial.
    campoDataInicial.value = "";

    // Limpa a data final.
    campoDataFinal.value = "";

    // Remove mensagens de validação das datas.
    campoDataInicial.setCustomValidity("");
    campoDataFinal.setCustomValidity("");

    // Atualiza a tabela com todas as movimentações.
    aplicarPesquisa();

});

// Busca as movimentações no Backend.
async function carregarMovimentacoes() {

    try {

        const resposta = await fetch("/api/movimentacoes");

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar as movimentações.");
        }

        movimentacoesCarregadas = await resposta.json();
        carregarCategorias();

        console.log(
            "Movimentações recebidas:",
            movimentacoesCarregadas
        );


        // Calculando receitas e despesas.
        let totalReceitas = 0;

        let totalDespesas = 0;

        movimentacoesCarregadas.forEach(function(movimentacao) {

            const valor = Number(movimentacao.valor);

            if (movimentacao.tipo === "entrada") {
                totalReceitas += valor;
            }

            if (movimentacao.tipo === "saida") {
                totalDespesas += valor;
            }

        });


        // Calculando o saldo.
        const saldo = totalReceitas - totalDespesas;


        // Atualizando os cartões financeiros.
        elementoSaldo.textContent = formatarMoeda(saldo);

        elementoReceitas.textContent = formatarMoeda(totalReceitas);

        elementoDespesas.textContent = formatarMoeda(totalDespesas);


        // Atualizando a tabela conforme a pesquisa atual.
        aplicarPesquisa();


    } catch (erro) {

        console.error("Erro ao carregar movimentações:", erro);

        exibirNotificacao(
            "Erro ao carregar dados!",
            erro.message,
            "erro"
        );

    }

}


/* 8. CARREGANDO OS DADOS AO ABRIR A PÁGINA */

carregarMovimentacoes();


/* 9. CONTROLE DO FORMULÁRIO */

// Selecionando os elementos HTML.

const formularioSecao = document.querySelector(
    "#formulario-movimentacao"
);

const formulario = document.querySelector(
    "#form-movimentacao"
);

const botaoCancelar = document.querySelector(
    "#cancelar-formulario"
);

const botaoEnviar = formulario.querySelector(
    'button[type="submit"]'
);


// Controla o estado do botão durante as operações.

function controlarBotaoEnviar(carregando, texto = "Cadastrar movimentação") {

    botaoEnviar.disabled = carregando;

    botaoEnviar.textContent = carregando
        ? "Salvando..."
        : texto;

}


// Valida os dados preenchidos no formulário.

function validarFormulario() {

    const descricao = campoDescricao.value.trim();

    const valor = Number(campoValor.value);

    const categoria = campoCategoria.value.trim();

    const data = campoData.value;

    // Verifica a descrição.
    if (!descricao) {
        return "Informe a descrição da movimentação.";
    }

    // Verifica o valor.
    if (!campoValor.value || !Number.isFinite(valor) || valor <= 0) {
        return "Informe um valor válido maior que zero.";
    }

    // Verifica a categoria.
    if (!categoria) {
        return "Informe a categoria da movimentação.";
    }

    // Verifica o tipo.
    if (
        campoTipo.value !== "entrada" &&
        campoTipo.value !== "saida"
    ) {
        return "Selecione um tipo de movimentação válido.";
    }

    // Verifica a data.
    if (!data) {
        return "Informe a data da movimentação.";
    }

    return null;

}

/* 10. ABRIR O FORMULÁRIO */

botaoPrincipal.addEventListener("click", function() {

    formularioSecao.hidden = false;

    formularioSecao.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

    identificadorParaEditar = null;

    formulario.reset();

    botaoEnviar.textContent = "Cadastrar movimentação";

});


/* 11. FECHAR O FORMULÁRIO */

botaoCancelar.addEventListener("click", function() {

    formularioSecao.hidden = true;

    formulario.reset();

    identificadorParaEditar = null;

    botaoEnviar.textContent = "Cadastrar movimentação";

});


/* 12. CADASTRAR E ATUALIZAR MOVIMENTAÇÕES */

formulario.addEventListener("submit", async function(event) {

    // Impede que o navegador recarregue a página.
    event.preventDefault();

    // Verifica se os dados preenchidos são válidos.
    const erroValidacao = validarFormulario();

    if (erroValidacao) {

        exibirNotificacao(
            "Verifique os dados!",
            erroValidacao,
            "erro"
        );

        return;

    }

    // Captura os valores preenchidos no formulário.
    const descricao = campoDescricao.value;
    const valor = campoValor.value;
    const tipo = campoTipo.value;
    const categoria = campoCategoria.value;
    const data = campoData.value;

    // Organiza os dados em um objeto JavaScript.
    const movimentacao = {
        descricao: descricao,
        valor: valor,
        tipo: tipo,
        categoria: categoria,
        data: data
    };

    // Verifica se estamos cadastrando ou editando.
    const estaEditando = identificadorParaEditar !== null;

    // Define o endereço da requisição.
    const url = estaEditando
        ? `/api/movimentacoes/${identificadorParaEditar}`
        : "/api/movimentacoes";

    // Define o método HTTP.
    const metodo = estaEditando ? "PUT" : "POST";

    // Desativa o botão enquanto os dados são enviados.
    controlarBotaoEnviar(true);

    try {

        // Envia os dados para o Backend Flask.
        const resposta = await fetch(url, {

            method: metodo,

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(movimentacao)

        });

        // Converte a resposta do Backend para JSON.
        const resultado = await resposta.json();

        // Verifica se ocorreu algum erro.
        if (!resposta.ok) {

            throw new Error(
                resultado.erro || "Não foi possível salvar a movimentação."
            );

        }

        // Informa o resultado da operação.
        exibirNotificacao(
            "Operação realizada!",
            resultado.mensagem,
            "sucesso"
        );

        // Limpa os campos do formulário.
        formulario.reset();

        // Fecha o formulário.
        formularioSecao.hidden = true;

        // Limpa o ID da edição.
        identificadorParaEditar = null;

        botaoEnviar.textContent = "Cadastrar movimentação";

        // Atualiza os dados do Dashboard.
        await carregarMovimentacoes();

    } catch (erro) {

        exibirNotificacao(
            "Erro ao salvar!",
            erro.message,
            "erro"
        );

    } finally {

        // Reativa o botão independentemente do resultado.
        controlarBotaoEnviar(
            false,
            identificadorParaEditar !== null
                ? "Salvar alterações"
                : "Cadastrar movimentação"
        );

    }

});

/* 13. MODAL DE CONFIRMAÇÃO DE EXCLUSÃO */

// Selecionando os elementos do modal.

// Seleciona a tabela de movimentações.
const listaMovimentacoes = document.querySelector(
    "#lista-movimentacoes"
);

const modalExclusao = document.querySelector("#modal-exclusao");

const botaoCancelarExclusao = document.querySelector(
    "#cancelar-exclusao"
);

const botaoConfirmarExclusao = document.querySelector(
    "#confirmar-exclusao"
);

// Guarda o ID da movimentação selecionada.
let identificadorParaExcluir = null;


/* 14. ABRIR O MODAL */

listaMovimentacoes.addEventListener("click", function(event) {

    if (event.target.classList.contains("btn-excluir")) {

        identificadorParaExcluir = event.target.dataset.id;

        modalExclusao.hidden = false;

        botaoConfirmarExclusao.focus();

    }

});


/* 15. FECHAR O MODAL */

function fecharModalExclusao() {

    modalExclusao.hidden = true;

    identificadorParaExcluir = null;

}

botaoCancelarExclusao.addEventListener("click", function() {

    fecharModalExclusao();

});


// Fechar ao clicar fora da caixa.

modalExclusao.addEventListener("click", function(event) {

    if (event.target === modalExclusao) {

        fecharModalExclusao();

    }

});


// Fechar ao pressionar ESC.

document.addEventListener("keydown", function(event) {

    if (event.key === "Escape" && !modalExclusao.hidden) {

        fecharModalExclusao();

    }

});


/* 15. CONFIRMAR A EXCLUSÃO */

botaoConfirmarExclusao.addEventListener("click", async function() {

    if (identificadorParaExcluir === null) {
        return;
    }

    const identificador = identificadorParaExcluir;

    botaoConfirmarExclusao.disabled = true;

    try {

        const resposta = await fetch(
            `/api/movimentacoes/${identificador}`,
            {
                method: "DELETE"
            }
        );

        const resultado = await resposta.json();

        if (!resposta.ok) {

            throw new Error(
                resultado.erro || "Não foi possível excluir."
            );

        }

        fecharModalExclusao();

        // Atualiza os dados do Dashboard.
        await carregarMovimentacoes();

        // Exibe uma notificação de sucesso.
        exibirNotificacao(
            "Exclusão realizada!",
            resultado.mensagem,
            "sucesso"
        );

    } catch (erro) {

        exibirNotificacao(
            "Erro ao excluir!",
            erro.message,
            "erro"
        );

    } finally {

        botaoConfirmarExclusao.disabled = false;

    }

});

/* 16. PREPARANDO A EDIÇÃO DE MOVIMENTAÇÕES */

// Guarda o ID da movimentação que está sendo editada.
let identificadorParaEditar = null;

// Selecionando os campos do formulário.
const campoDescricao = document.querySelector("#descricao");
const campoValor = document.querySelector("#valor");
const campoTipo = document.querySelector("#tipo");
const campoCategoria = document.querySelector("#categoria");
const campoData = document.querySelector("#data");

// Selecionando os elementos do modal de edição.
const modalEdicao = document.querySelector("#modal-edicao");

const botaoCancelarEdicao = document.querySelector(
    "#cancelar-edicao"
);

const botaoConfirmarEdicao = document.querySelector(
    "#confirmar-edicao"
);

// Detectando cliques nos botões Editar.
listaMovimentacoes.addEventListener("click", function(event) {

    if (event.target.classList.contains("btn-editar")) {

        // Identifica qual movimentação foi selecionada.
        const identificador = Number(event.target.dataset.id);

        // Guarda o ID da movimentação selecionada.
        identificadorParaEditar = identificador;

        // Abre o modal de confirmação.
        modalEdicao.hidden = false;

        // Coloca o foco no botão de confirmação.
        botaoConfirmarEdicao.focus();

    }

});

// Busca e preenche os dados da movimentação selecionada.
async function carregarMovimentacoesParaEdicao(identificador) {

    try {

        const resposta = await fetch("/api/movimentacoes");

        if (!resposta.ok) {
            throw new Error("Não foi possível buscar as movimentações.");
        }

        const movimentacoes = await resposta.json();

        const movimentacao = movimentacoes.find(function(item) {
            return item.id === identificador;
        });

        if (!movimentacao) {
            throw new Error("Movimentação não encontrada.");
        }

        // Guarda o ID que será atualizado posteriormente.
        identificadorParaEditar = movimentacao.id;

        // Preenche os campos do formulário.
        campoDescricao.value = movimentacao.descricao;
        campoValor.value = movimentacao.valor;
        campoTipo.value = movimentacao.tipo;
        campoCategoria.value = movimentacao.categoria;
        campoData.value = movimentacao.data;

        // Altera o texto do botão para indicar que estamos editando.
        botaoEnviar.textContent = "Salvar alterações";
        // Abre o formulário.
        formularioSecao.hidden = false;

        formularioSecao.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (erro) {
        console.error("Erro ao carregar movimentação:", erro);

        exibirNotificacao(
            "Erro ao carregar movimentação!",
            erro.message,
            "erro"
        );
    }

}

/* 17. CONTROLE DO MODAL DE EDIÇÃO */

// Função para fechar o modal.
function fecharModalEdicao() {

    modalEdicao.hidden = true;

    identificadorParaEditar = null;

}


// Botão cancelar.
botaoCancelarEdicao.addEventListener("click", function() {

    fecharModalEdicao();

});


// Fechar ao clicar fora da caixa.
modalEdicao.addEventListener("click", function(event) {

    if (event.target === modalEdicao) {

        fecharModalEdicao();

    }

});


// Fechar ao pressionar ESC.
document.addEventListener("keydown", function(event) {

    if (event.key === "Escape" && !modalEdicao.hidden) {

        fecharModalEdicao();

    }

});


// Confirmar a edição.
botaoConfirmarEdicao.addEventListener("click", async function() {

    if (identificadorParaEditar === null) {
        return;
    }

    const identificador = identificadorParaEditar;

    // Fecha o modal.
    fecharModalEdicao();

    // Carrega os dados no formulário.
    await carregarMovimentacoesParaEdicao(identificador);

});