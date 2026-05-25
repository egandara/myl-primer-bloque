using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;

namespace SandboxApp.Hubs
{
    public class GameHub : Hub
    {
        public async Task UnirseAPartida(string codigoSala, string nombreGladiador)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, codigoSala);
            await Clients.OthersInGroup(codigoSala).SendAsync("RecibirNotificacion", $"El gladiador [{nombreGladiador}] ingresó a la arena de combate.");
        }

        public async Task EnviarMensajeSala(string codigoSala, string remitente, string mensaje)
        {
            await Clients.Group(codigoSala).SendAsync("RecibirMensajeChat", $"{remitente}: {mensaje}");
        }

        public async Task SincronizarTableroMesa(string codigoSala, string jsonCartasTablero)
        {
            await Clients.OthersInGroup(codigoSala).SendAsync("RecibirTableroSincronizado", jsonCartasTablero);
        }

        public async Task SincronizarLogTactico(string codigoSala, string logEntrada)
        {
            await Clients.OthersInGroup(codigoSala).SendAsync("RecibirLogSincronizado", logEntrada);
        }
    }
}