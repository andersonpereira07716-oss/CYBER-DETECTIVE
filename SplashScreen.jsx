import React, { useState, useEffect } from 'react';

export default function SplashScreen({ onStartGame }) {
  const [progress, setProgress] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  // Simula o carregamento dos arquivos do jogo ao abrir o app
  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress >= 100) {
          clearInterval(interval);
          setIsLoaded(true);
          return 100;
        }
        // Incrementa a barra de progresso aleatoriamente
        const diff = Math.floor(Math.random() * 15) + 5;
        return Math.min(oldProgress + diff, 100);
      });
    }, 200);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-black flex flex-col justify-between items-center select-none">
      
      {/* Imagem de Fundo (Substitua o caminho pelo nome do arquivo salvo no seu projeto) */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-85"
        style={{ backgroundImage: `url('/assets/splash_background.png')` }}
      />

      {/* Camada de escurecimento / vinheta para dar o tom noir/suspense */}
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-black/70 pointer-events-none" />

      {/* TOPO: Título do Jogo */}
      <div className="relative z-10 pt-8 text-center px-4">
        <h1 className="text-zinc-100 font-serif tracking-widest text-2xl md:text-4xl drop-shadow-[0_2px_10px_rgba(0,0,0,0.9)]">
          SHADOWS OF EVIDENCE
        </h1>
        <p className="text-red-600 font-mono text-xs md:text-sm tracking-[0.3em] uppercase mt-1">
          criminal investigation RPG
        </p>
      </div>

      {/* CENTRO: Espaço livre para aproveitar a arte do quadro de evidências */}
      <div className="relative z-10 flex-grow flex items-center justify-center">
        {/* Aqui você pode colocar um aviso sutil ou deixar a arte respirar */}
      </div>

      {/* RODAPÉ: Barra de Carregamento ou Botão de Ação */}
      <div className="relative z-10 pb-10 w-full max-w-xs md:max-w-md px-6 flex flex-col items-center">
        
        {!isLoaded ? (
          /* Estado de Carregamento */
          <div className="w-full bg-zinc-900/80 border border-zinc-700/50 rounded p-3 backdrop-blur-sm shadow-xl">
            <div className="flex justify-between text-xs font-mono text-emerald-400 mb-1.5">
              <span>CARREGANDO CASOS...</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-zinc-950 h-2 rounded-full overflow-hidden border border-zinc-800">
              <div 
                className="bg-emerald-500 h-full transition-all duration-200 ease-out shadow-[0_0_10px_#10b981]"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        ) : (
          /* Botão Pronto para Iniciar */
          <button
            onClick={onStartGame}
            className="w-full py-4 bg-zinc-900/90 hover:bg-zinc-800 border border-red-600/60 hover:border-red-500 text-zinc-100 font-mono tracking-[0.2em] uppercase text-sm rounded transition-all duration-300 shadow-[0_0_20px_rgba(220,38,38,0.3)] animate-pulse active:scale-95"
          >
            TAP TO CONTINUE
          </button>
        )}

        {/* Rodapé institucional pequeno */}
        <span className="text-[10px] font-mono text-zinc-500 tracking-widest mt-4 uppercase">
          Presented by Noir Games
        </span>
      </div>

    </div>
  );
}
