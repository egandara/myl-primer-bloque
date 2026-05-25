using System.Collections.Generic;

namespace SandboxApp.Models
{
    public class ProgresoJugador
    {
        public string NombreGladiador { get; set; } = "Gladiador";
        public int Oro { get; set; } = 1500; // Monedas iniciales (alcanza para 3 sobres de $500)
        public int Victorias { get; set; } = 0;
        public int Derrotas { get; set; } = 0;

        // Almacena: [Nombre de la Carta] -> [Cantidad de copias que posees]
        public Dictionary<string, int> Coleccion { get; set; } = new Dictionary<string, int>();

        // Lista de nombres de las cartas que componen tu mazo activo de campaña
        public List<string> MazoCampana { get; set; } = new List<string>();

        // Saber si ya se le entregó el mazo de cartas Vasallas iniciales gratis
        public bool RecibioKitInicial { get; set; } = false;
    }
}