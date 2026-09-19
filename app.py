from flask import Flask, render_template_string, jsonify, request
import json

app = Flask(__name__)

# Base de Dados de Casos com suporte a expansão dinâmica (JSON)
CASOS = {
    "1": {
        "titulo": "Caso 01: Vazamento na Nexus Corp",
        "dificuldade": "Fácil",
        "tempo_limite": 120,
        "premio": 500,
        "premium": False,
        "descricao": "Dados sigilosos vazaram na dark web. Descubra quem vendeu o acesso interno.",
        "suspeitos": [
            {"nome": "Carlos Silva", "cargo": "Analista de Redes", "perfil": "Acessou o servidor às 02:00 AM.", "culpado": False},
            {"nome": "Beatriz Mendes", "cargo": "Diretora Financeira", "perfil": "Suas credenciais foram usadas no terminal principal.", "culpado": True},
            {"nome": "Marcos Lima", "cargo": "Estagiário de TI", "perfil": "Tentou burlar o firewall ontem à tarde.", "culpado": False}
        ],
        "acessos": [
            {"ip": "192.168.1.45", "usuario": "carlos.silva", "hora": "01:55", "status": "Autorizado"},
            {"ip": "10.0.0.12", "usuario": "beatriz.mendes", "hora": "02:14", "status": "Forçado (Criptografado)"},
            {"ip": "172.16.0.8", "usuario": "marcos.lima", "hora": "03:30", "status": "Negado"}
        ],
        "pistas": [
            "O invasor utilizou uma VPN corporativa interna.",
            "A senha do terminal principal foi alterada 10 minutos antes do ataque.",
            "Há arquivos criptografados no diretório do suspeito culpado."
        ],
        "dica_central": "Inspecione os registos de IP e cruze com o cargo de liderança que tinha acesso direto ao terminal principal.",
        "senha_hack": "NEXUS2026"
    },
    "2": {
        "titulo": "Caso 02: Sabotagem Satelital",
        "dificuldade": "Médio",
        "tempo_limite": 90,
        "premio": 900,
        "premium": False,
        "descricao": "O satélite orbital de comunicações sofreu uma sobrecarga intencional de energia.",
        "suspeitos": [
            {"nome": "Dr. Arnaldo Tech", "cargo": "Engenheiro Chefe", "perfil": "Reclamou de cortes no orçamento.", "culpado": False},
            {"nome": "Helena Vane", "cargo": "Especialista em Órbitas", "perfil": "Possui acesso direto aos códigos de propulsão.", "culpado": True},
            {"nome": "Igor Petrov", "cargo": "Técnico de Manutenção", "perfil": "Ausente do posto durante o pico.", "culpado": False}
        ],
        "acessos": [
            {"ip": "200.150.3.10", "usuario": "helena.vane", "hora": "23:10", "status": "Comando de Sobrecarga Enviado"},
            {"ip": "200.150.3.15", "usuario": "arnaldo.tech", "hora": "21:00", "status": "Diagnóstico de Rotina"}
        ],
        "pistas": [
            "O comando veio de uma chave criptografada de nível 3.",
            "Helena atualizou seus registros de ponto logo após o alerta."
        ],
        "dica_central": "Verifique qual dos suspeitos tinha a atribuição exata ligada à propulsão e alteração de órbitas.",
        "senha_hack": "ORBITA99"
    },
    "3": {
        "titulo": "Caso 03: Sequestro da IA AURA",
        "dificuldade": "Difícil",
        "tempo_limite": 60,
        "premio": 1500,
        "premium": True,
        "descricao": "A IA central 'AURA' foi isolada por um ransomware desconhecido na rede.",
        "suspeitos": [
            {"nome": "Satoshi Ghost", "cargo": "Pesquisador Autônomo", "perfil": "Defensor do livre acesso à IA.", "culpado": True},
            {"nome": "Clara Vance", "cargo": "Ética em IA", "perfil": "Pediu o desligamento da AURA na semana passada.", "culpado": False}
        ],
        "acessos": [
            {"ip": "127.0.0.1", "usuario": "satoshi.ghost", "hora": "04:00", "status": "Injeção de Ransomware"}
        ],
        "pistas": [
            "O código do ransomware contém assinaturas de um fórum underground.",
            "A chave de descriptografia está oculta nos logs do servidor."
        ],
        "dica_central": "A ideologia e o histórico de ativismo digital pesam fortemente contra o pesquisador autônomo.",
        "senha_hack": "AURA_FREE"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER-DETECTIVE v9.0 ULTIMATE</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Courier New', Courier, monospace; }
        body { background-color: #0b0f19; color: #00ffcc; padding: 12px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 500px; }
        header { text-align: center; margin-bottom: 8px; border-bottom: 1px dashed #00ffcc; padding-bottom: 6px; }
        h1 { font-size: 1.2rem; letter-spacing: 1px; color: #00ffcc; text-shadow: 0 0 6px rgba(0,255,204,0.4); }
        .subtitle { font-size: 0.68rem; color: #8892b0; margin-top: 2px; }
        
        .top-stats { display: flex; justify-content: space-between; font-size: 0.73rem; background: #111827; padding: 6px 10px; border-radius: 4px; border: 1px solid #1f293d; margin-bottom: 6px; }
        .badges-row { display: flex; gap: 4px; font-size: 0.65rem; background: rgba(255,187,0,0.05); padding: 4px 8px; border-radius: 4px; border: 1px dashed #ffbb00; margin-bottom: 8px; color: #ffbb00; justify-content: space-between; align-items: center; }

        .panel { background: #111827; border: 1px solid #1f293d; border-radius: 6px; padding: 10px; margin-bottom: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .flex-between { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
        label { font-size: 0.72rem; color: #8892b0; display: block; margin-bottom: 3px; }
        select { width: 100%; background: #0b0f19; color: #00ffcc; border: 1px solid #00ffcc; padding: 7px; border-radius: 4px; font-size: 0.78rem; outline: none; }
        
        .timer-box { font-size: 0.8rem; color: #ff5555; font-weight: bold; background: rgba(255,85,85,0.1); padding: 4px 8px; border-radius: 4px; border: 1px solid #ff5555; white-space: nowrap; }
        .timer-pulse { animation: pulseWarning 1s infinite; }
        @keyframes pulseWarning { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }

        .grid-buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-bottom: 8px; }
        button { background: transparent; color: #00ffcc; border: 1px solid #00ffcc; padding: 7px; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 0.78rem; transition: 0.2s; }
        button:active { background: rgba(0,255,204,0.2); }
        button.danger { color: #ff5555; border-color: #ff5555; grid-column: span 2; }
        button.accent { color: #ffbb00; border-color: #ffbb00; }
        button.info { color: #38bdf8; border-color: #38bdf8; }
        button.store { color: #c084fc; border-color: #c084fc; grid-column: span 2; }

        .terminal-output { background: #05070d; border: 1px solid #1f293d; border-radius: 4px; padding: 8px; min-height: 120px; max-height: 160px; overflow-y: auto; font-size: 0.78rem; line-height: 1.4; color: #c3ceed; white-space: pre-wrap; }
        
        .terminal-input-row { display: flex; gap: 5px; margin-top: 6px; }
        .terminal-input-row input { flex: 1; background: #05070d; border: 1px solid #1f293d; color: #00ffcc; padding: 6px; border-radius: 4px; outline: none; font-size: 0.78rem; }
        .terminal-input-row button { width: 65px; padding: 6px; }

        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); justify-content: center; align-items: center; padding: 15px; z-index: 99; }
        .modal-content { background: #111827; border: 1px solid #00ffcc; padding: 15px; border-radius: 6px; width: 100%; max-width: 350px; text-align: center; }
        .modal-content input { width: 100%; padding: 8px; background: #05070d; border: 1px solid #00ffcc; color: #00ffcc; margin: 10px 0; text-align: center; font-size: 1rem; border-radius: 4px; outline: none; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>CYBER-DETECTIVE ULTIMATE</h1>
            <div class="subtitle">v9.0 • Badges, Paywall Real & Synth Engine</div>
        </header>

        <div class="top-stats">
            <span>🛡️ Reputação: <b id="scoreDisplay" style="color: #ffbb00;">0</b> pts</span>
            <span>🏆 Resolvidos: <b id="casosResolvidosCount">0</b></span>
        </div>

        <div class="badges-row">
            <span>🏅 Badges: <b id="badgeCount">0</b>/3</span>
            <span id="badgeStatus" style="font-size: 0.62rem; color: #8892b0;">Nenhuma conquista ainda</span>
        </div>

        <div class="panel">
            <div class="flex-between">
                <div style="flex: 1; margin-right: 10px;">
                    <label for="casoSelect">SELECIONAR CASO:</label>
                    <select id="casoSelect" onchange="mudarCaso()">
                        {% for id, caso in casos.items() %}
                        <option value="{{ id }}">{{ caso.titulo }} {% if caso.premium %}👑 [VIP]{% endif %}</option>
                        {% endfor %}
                    </select>
                </div>
                <div>
                    <label>TEMPO:</label>
                    <div id="timerDisplay" class="timer-box">--:--</div>
                </div>
            </div>
            <div style="margin-top: 6px; font-size: 0.72rem; color: #8892b0;" id="casoDesc"></div>
        </div>

        <div class="panel">
            <div class="grid-buttons">
                <button onclick="tocarSom('click'); carregarDados('suspeitos')">Suspeitos</button>
                <button onclick="tocarSom('click'); carregarDados('acessos')">Acessos</button>
                <button onclick="tocarSom('click'); carregarDados('pistas')">Pistas</button>
                <button class="info" onclick="tocarSom('click'); pedirDica()">💡 Dica IA (-12s)</button>
                <button class="accent" onclick="tocarSom('click'); abrirMiniGame()">🔓 Hackear Servidor</button>
                <button class="danger" onclick="tocarSom('click'); abrirAcusar()">Acusar Culpado</button>
                <button class="store" onclick="tocarSom('click'); abrirLojaVIP()">👑 Desbloquear Passe VIP (Checkout)</button>
            </div>

            <label>LOG DO TERMINAL:</label>
            <div id="terminalOutput" class="terminal-output">Selecione uma opção acima ou digite comandos...</div>
            
            <div class="terminal-input-row">
                <input type="text" id="cmdInput" placeholder="cmd (ex: help, status)..." onkeypress="checarEnter(event)">
                <button onclick="executarComando()">Enviar</button>
            </div>
        </div>
    </div>

    <!-- Modais -->
    <div id="modalHack" class="modal">
        <div class="modal-content">
            <h3 style="color: #ffbb00; margin-bottom: 8px; font-size: 1rem;">🔓 DESCRYPTOR DE SENHA</h3>
            <p style="font-size: 0.75rem; color: #8892b0;">Insira a chave extraída nas pistas:</p>
            <input type="text" id="senhaInput" placeholder="SENHA">
            <button style="width: 100%;" onclick="tentarHackear()">DESBLOQUEAR</button>
            <button style="width: 100%; margin-top: 6px; border-color: #8892b0; color: #8892b0;" onclick="fecharModal('modalHack')">Cancelar</button>
        </div>
    </div>

    <div id="modalAcusar" class="modal">
        <div class="modal-content">
            <h3 style="color: #ff5555; margin-bottom: 8px; font-size: 1rem;">⚠️ ACUSAÇÃO OFICIAL</h3>
            <p style="font-size: 0.75rem; color: #8892b0; margin-bottom: 8px;">Quem é o verdadeiro criminoso?</p>
            <div id="listaSuspeitosAcusar" style="display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px;"></div>
            <button style="width: 100%; border-color: #ff5555; color: #ff5555;" onclick="fecharModal('modalAcusar')">Voltar</button>
        </div>
    </div>

    <div id="modalRelatorio" class="modal">
        <div class="modal-content">
            <h3 id="tituloRelatorio" style="color: #00ffcc; margin-bottom: 8px; font-size: 1.1rem;">RELATÓRIO</h3>
            <p id="textoRelatorio" style="font-size: 0.8rem; color: #c3ceed; margin-bottom: 12px; line-height: 1.4;"></p>
            <button style="width: 100%;" onclick="fecharModal('modalRelatorio')">CONTINUAR</button>
        </div>
    </div>

    <div id="modalLoja" class="modal">
        <div class="modal-content">
            <h3 style="color: #c084fc; margin-bottom: 8px; font-size: 1.1rem;">👑 CHECKOUT VIP COMERCIAL</h3>
            <p style="font-size: 0.78rem; color: #c3ceed; margin-bottom: 12px; line-height: 1.4;">
                Deseja adquirir o acesso vitalício a todos os casos avançados? (Simulação de integração com gateway de pagamento Pix/Mercado Pago).
            </p>
            <button style="width: 100%; border-color: #c084fc; color: #c084fc; margin-bottom: 6px;" onclick="irParaPagamentoReal()">PAGAR VIA PIX / CARTÃO</button>
            <button style="width: 100%; border-color: #8892b0; color: #8892b0;" onclick="fecharModal('modalLoja')">Voltar</button>
        </div>
    </div>

    <script>
        let casoAtualId = "1";
        let tempoRestante = 120;
        let timerInterval = null;
        let jogoAtivo = true;
        let scoreTotal = parseInt(localStorage.getItem('cyber_score') || '0');
        let casosResolvidos = parseInt(localStorage.getItem('cyber_solved') || '0');
        let vipDesbloqueado = localStorage.getItem('cyber_vip') === 'true';
        let badges = JSON.parse(localStorage.getItem('cyber_badges') || '{"hacker":false, "relampago":false, "mestre":false}');

        const dadosCasos = {{ casos_json | safe }};

        document.getElementById('scoreDisplay').innerText = scoreTotal;
        document.getElementById('casosResolvidosCount').innerText = casosResolvidos;
        atualizarPainelBadges();

        // Motor Synth Web Audio Avançado
        function tocarSom(tipo) {
            try {
                let ctx = new (window.AudioContext || window.webkitAudioContext)();
                let osc = ctx.createOscillator();
                let gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);

                if (tipo === 'click') {
                    osc.frequency.setValueAtTime(800, ctx.currentTime);
                    gain.gain.setValueAtTime(0.03, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
                    osc.start(); osc.stop(ctx.currentTime + 0.08);
                } else if (tipo === 'sucesso') {
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(440, ctx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.2);
                    gain.gain.setValueAtTime(0.05, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
                    osc.start(); osc.stop(ctx.currentTime + 0.25);
                } else if (tipo === 'erro') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, ctx.currentTime);
                    osc.frequency.linearRampToValueAtTime(80, ctx.currentTime + 0.3);
                    gain.gain.setValueAtTime(0.06, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
                    osc.start(); osc.stop(ctx.currentTime + 0.3);
                }
            } catch(e) {}
        }

        function iniciarTimer(segundos) {
            clearInterval(timerInterval);
            tempoRestante = segundos;
            atualizarDisplayTempo();
            
            timerInterval = setInterval(() => {
                if (!jogoAtivo) return;
                tempoRestante--;
                atualizarDisplayTempo();

                let timerBox = document.getElementById('timerDisplay');
                if (tempoRestante <= 15) {
                    timerBox.classList.add('timer-pulse');
                    if (navigator.vibrate) navigator.vibrate(80);
                } else {
                    timerBox.classList.remove('timer-pulse');
                }

                if (tempoRestante <= 0) {
                    clearInterval(timerInterval);
                    jogoAtivo = false;
                    tocarSom('erro');
                    timerBox.classList.remove('timer-pulse');
                    escreverTerminal("⚠️ TEMPO ESGOTADO! Servidor formatado.");
                    mostrarRelatorio("FALHA NA MISSÃO", "O tempo esgotou-se. Perdeu o acesso ao servidor.");
                }
            }, 1000);
        }

        function atualizarDisplayTempo() {
            let min = Math.floor(tempoRestante / 60);
            let sec = tempoRestante % 60;
            document.getElementById('timerDisplay').innerText = 
                (min < 10 ? "0" + min : min) + ":" + (sec < 10 ? "0" + sec : sec);
        }

        function mudarCaso() {
            casoAtualId = document.getElementById('casoSelect').value;
            let caso = dadosCasos[casoAtualId];

            if (caso.premium && !vipDesbloqueado) {
                abrirLojaVIP();
                return;
            }

            document.getElementById('casoDesc').innerText = caso.descricao;
            jogoAtivo = true;
            iniciarTimer(caso.tempo_limite);
            escreverTerminal(">>> SISTEMA CARREGADO: " + caso.titulo + "\\n> Digite 'help' para comandos.");
        }

        function escreverTerminal(texto) {
            let out = document.getElementById('terminalOutput');
            out.innerText = texto;
            out.scrollTop = out.scrollHeight;
        }

        function carregarDados(tipo) {
            if (!jogoAtivo) return;
            let caso = dadosCasos[casoAtualId];
            let texto = "";

            if (tipo === 'suspeitos') {
                texto = "=== SUSPEITOS ===\\n\\n";
                caso.suspeitos.forEach((s, idx) => {
                    texto += `[${idx+1}] ${s.nome} (${s.cargo})\\n    Perfil: ${s.perfil}\\n\\n`;
                });
            } else if (tipo === 'acessos') {
                texto = "=== REGISTROS DE IP ===\\n\\n";
                caso.acessos.forEach(a => {
                    texto += `IP: ${a.ip} | User: ${a.usuario}\\nHora: ${a.hora} | Status: ${a.status}\\n----------------------------\\n`;
                });
            } else if (tipo === 'pistas') {
                texto = "=== PISTAS ===\\n\\n";
                caso.pistas.forEach((p, idx) => {
                    texto += `(Pista ${idx+1}) ${p}\\n`;
                });
            }
            escreverTerminal(texto);
        }

        function pedirDica() {
            if (!jogoAtivo) return;
            let caso = dadosCasos[casoAtualId];
            tempoRestante -= 12;
            if(tempoRestante < 0) tempoRestante = 0;
            atualizarDisplayTempo();
            escreverTerminal(`💡 DICA DA CENTRAL:\\n> ${caso.dica_central}\\n\\n(⚠️ Penalidade: -12s)`);
        }

        function abrirMiniGame() {
            if (!jogoAtivo) return;
            document.getElementById('modalHack').style.display = 'flex';
            document.getElementById('senhaInput').value = '';
        }

        function fecharModal(id) {
            document.getElementById(id).style.display = 'none';
        }

        function tentarHackear() {
            let senha = document.getElementById('senhaInput').value;
            let caso = dadosCasos[casoAtualId];
            fecharModal('modalHack');
            if (senha === caso.senha_hack) {
                tocarSom('sucesso');
                escreverTerminal("🔓 SUCESSO! Acesso root concedido.");
                if (!badges.hacker) {
                    badges.hacker = true;
                    scoreTotal += 300;
                    salvarProgresso();
                    atualizarPainelBadges();
                    alert("🏅 Badge Desbloqueada: 💻 Hacker Elite (+300 pts)!");
                }
            } else {
                tocarSom('erro');
                escreverTerminal("❌ SENHA INCORRETA! -15 segundos.");
                tempoRestante -= 15;
            }
        }

        function abrirAcusar() {
            if (!jogoAtivo) return;
            let caso = dadosCasos[casoAtualId];
            let container = document.getElementById('listaSuspeitosAcusar');
            container.innerHTML = "";
            caso.suspeitos.forEach(s => {
                let btn = document.createElement('button');
                btn.innerText = s.nome + " (" + s.cargo + ")";
                btn.onclick = () => fazerAcusacao(s.culpado, s.nome);
                container.appendChild(btn);
            });
            document.getElementById('modalAcusar').style.display = 'flex';
        }

        function fazerAcusacao(culpado, nome) {
            fecharModal('modalAcusar');
            clearInterval(timerInterval);
            jogoAtivo = false;
            let caso = dadosCasos[casoAtualId];

            if (culpado) {
                tocarSom('sucesso');
                escreverTerminal(`🎉 PARABÉNS! ${nome} era o culpado!`);
                scoreTotal += caso.premio;
                casosResolvidos++;

                if (!badges.mestre) {
                    badges.mestre = true;
                    scoreTotal += 500;
                }
                if (tempoRestante >= 30 && !badges.relampago) {
                    badges.relampago = true;
                    scoreTotal += 400;
                }

                salvarProgresso();
                document.getElementById('scoreDisplay').innerText = scoreTotal;
                document.getElementById('casosResolvidosCount').innerText = casosResolvidos;
                atualizarPainelBadges();

                mostrarRelatorio("CASO RESOLVIDO COM SUCESSO", `O suspeito ${nome} foi detido. Ganhou +${caso.premio} pontos!`);
            } else {
                tocarSom('erro');
                escreverTerminal(`❌ FALHA! ${nome} era inocente.`);
                mostrarRelatorio("ERRO NA INVESTIGAÇÃO", `Acusação errada. O verdadeiro criminoso escapou.`);
            }
        }

        function mostrarRelatorio(titulo, texto) {
            document.getElementById('tituloRelatorio').innerText = titulo;
            document.getElementById('textoRelatorio').innerText = texto;
            document.getElementById('modalRelatorio').style.display = 'flex';
        }

        function abrirLojaVIP() {
            document.getElementById('modalLoja').style.display = 'flex';
        }

       function irParaPagamentoReal() {
    tocarSom('click');
    const linkMercadoPago = "https://mpago.la/1Z4Rypg"; 
    window.open(linkMercadoPago, '_blank');
}






        function salvarProgresso() {
            localStorage.setItem('cyber_score', scoreTotal);
            localStorage.setItem('cyber_solved', casosResolvidos);
            localStorage.setItem('cyber_badges', JSON.stringify(badges));
        }

        function atualizarPainelBadges() {
            let count = 0;
            if (badges.hacker) count++;
            if (badges.relampago) count++;
            if (badges.mestre) count++;
            document.getElementById('badgeCount').innerText = count;
            if (count > 0) {
                document.getElementById('badgeStatus').innerText = "Conquistas ativas e bonificadas";
            }
        }

        function checarEnter(event) {
            if (event.key === 'Enter') executarComando();
        }

        function executarComando() {
            if (!jogoAtivo) return;
            let input = document.getElementById('cmdInput');
            let cmd = input.value.trim().toLowerCase();
            input.value = "";

            if (cmd === 'help') {
                escreverTerminal("Comandos: status, clear, time, hack, dica");
            } else if (cmd === 'status') {
                let caso = dadosCasos[casoAtualId];
                escreverTerminal(`Caso: ${caso.titulo}\\nReputação: ${scoreTotal} pts`);
            } else if (cmd === 'clear') {
                escreverTerminal("Terminal limpo.");
            } else if (cmd === 'time') {
                escreverTerminal(`Tempo restante: ${tempoRestante}s`);
            } else if (cmd === 'hack') {
                abrirMiniGame();
            } else if (cmd === 'dica') {
                pedirDica();
            } else {
                escreverTerminal(`Comando inválido: '${cmd}'.`);
            }
        }

        window.onload = function() { mudarCaso(); };
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, casos=CASOS, casos_json=json.dumps(CASOS))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
