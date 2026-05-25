using System;
using System.Collections.Generic;
using SandboxApp.Components.Pages; // Necesario para acceder a Home.CartaJuego

namespace SandboxApp.Models
{
    public class GameState
    {
        // Identificador único de la sala (ej. "A4F2")
        public string SalaId { get; set; } = Guid.NewGuid().ToString().Substring(0, 4).ToUpper();

        // Nombres o IDs de los jugadores
        public string Jugador1 { get; set; } = "";
        public string Jugador2 { get; set; } = "";

        // Todas las cartas de la partida (las de ambos jugadores)
        public List<Home.CartaJuego> CartasEnJuego { get; set; } = new();

        // Chat e Historial compartidos
        public List<string> HistorialLogs { get; set; } = new();
        public List<string> MensajesChat { get; set; } = new();

        // Control de turnos
        public string JugadorTurnoActivo { get; set; } = "";

        // Evento mágico de Blazor para actualizar las pantallas de ambos jugadores al mismo tiempo
        public event Action? OnStateChanged;

        public void NotificarCambios()
        {
            OnStateChanged?.Invoke();
        }

        public void AgregarLog(string mensaje)
        {
            HistorialLogs.Add($"[{DateTime.Now.ToLongTimeString()}] {mensaje}");
            NotificarCambios();
        }

        public void EnviarMensaje(string jugador, string mensaje)
        {
            MensajesChat.Add($"{jugador}: {mensaje}");
            NotificarCambios();
        }
    }
}