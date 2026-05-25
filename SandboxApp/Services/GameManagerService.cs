using System;
using System.Collections.Concurrent;
using SandboxApp.Models;

namespace SandboxApp.Services
{
    public class GameManagerService
    {
        // Usamos ConcurrentDictionary porque en un entorno web varios jugadores pueden intentar crear partidas al mismo tiempo
        private readonly ConcurrentDictionary<string, GameState> _partidasActivas = new();

        // El Jugador 1 crea la partida
        public GameState CrearPartida(string nombreJugador)
        {
            var nuevaPartida = new GameState
            {
                Jugador1 = nombreJugador
            };

            nuevaPartida.AgregarLog($"Sala creada. Esperando a que el rival se una con el código: {nuevaPartida.SalaId}");

            _partidasActivas.TryAdd(nuevaPartida.SalaId, nuevaPartida);
            return nuevaPartida;
        }

        // Busca una partida por su código
        public GameState? ObtenerPartida(string salaId)
        {
            if (string.IsNullOrWhiteSpace(salaId)) return null;

            _partidasActivas.TryGetValue(salaId.ToUpper(), out var partida);
            return partida;
        }

        // El Jugador 2 se une usando el código
        public GameState? UnirseAPartida(string salaId, string nombreJugador)
        {
            var partida = ObtenerPartida(salaId);

            // Verificamos que la partida exista y que el espacio del Jugador 2 esté vacío
            if (partida != null && string.IsNullOrEmpty(partida.Jugador2))
            {
                partida.Jugador2 = nombreJugador;
                partida.AgregarLog($"[{nombreJugador}] se ha unido a la partida. ¡Que comience el duelo!");
                return partida;
            }

            return null; // Retorna null si la sala no existe o ya está llena
        }
    }
}