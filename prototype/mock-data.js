// TrashMap - Mock Data para Demo Standalone
// Venezuela environmental hot spots - 2026

const MOCK_REPORTS = [
    {
        id: 'demo-1',
        type: 'plastico',
        size: 'large',
        notes: 'Acumulación de plásticos en playa - aproximadamente 200kg',
        coords: [-58.3916, 10.4806], // Vargas/Aragua costero
        date: '2026-03-24',
        reporter: '@ecovoluntario',
        status: 'active'
    },
    {
        id: 'demo-2',
        type: 'electronico',
        size: 'medium',
        notes: 'Descarga ilegal de electrodomésticos en quebrada',
        coords: [-66.8792, 10.4806], // Caracas
        date: '2026-03-23',
        reporter: '@vecino23',
        status: 'active'
    },
    {
        id: 'demo-3',
        type: 'domestico',
        size: 'large',
        notes: 'Vertedero espontáneo creciendo - vecinos dumpando escombros',
        coords: [-68.0073, 10.1638], // Maracay
        date: '2026-03-22',
        reporter: '@ambientalista91',
        status: 'verified'
    },
    {
        id: 'demo-4',
        type: 'industrial',
        size: 'large',
        notes: 'Descarte de residuos industriales cerca del río',
        coords: [-71.5211, 10.6316], // Maracaibo
        date: '2026-03-21',
        reporter: '@ecochek',
        status: 'active'
    },
    {
        id: 'demo-5',
        type: 'plastico',
        size: 'medium',
        notes: 'Botadero a cielo abierto afectando mangrove',
        coords: [-64.6895, 10.1624], // Puerto La Cruz
        date: '2026-03-20',
        reporter: '@diasporavzlana',
        status: 'active'
    },
    {
        id: 'demo-6',
        type: 'domestico',
        size: 'small',
        notes: 'Micro-basurero en zona residencial',
        coords: [-67.4856, 9.5586], // Barquisimeto
        date: '2026-03-19',
        reporter: '@cleanupcrew',
        status: 'cleaned'
    },
    {
        id: 'demo-7',
        type: 'vidrio',
        size: 'medium',
        notes: 'Acumulación de vidrio roto en terreno abandonado',
        coords: [-63.5511, 8.6246], // Ciudad Bolívar
        date: '2026-03-18',
        reporter: '@turisteando',
        status: 'active'
    },
    {
        id: 'demo-8',
        type: 'papel',
        size: 'small',
        notes: 'Documentos institucionales abandonados (posible data sensible)',
        coords: [-66.9036, 10.5006], // Caracas - Sabana Grande
        date: '2026-03-17',
        reporter: '@seguridadfirst',
        status: 'verified'
    },
    {
        id: 'demo-9',
        type: 'plastico',
        size: 'large',
        notes: 'Sábanas de plástico agrícola en zona agrícola - riesgo de contaminación',
        coords: [-69.2323, 10.7287], // Yaritagua
        date: '2026-03-16',
        reporter: '@agrupueblo',
        status: 'active'
    },
    {
        id: 'demo-10',
        type: 'electronico',
        size: 'medium',
        notes: 'Baterías y cables abandonados - riesgo químico',
        coords: [-65.5428, 10.2136], // Valencia
        date: '2026-03-15',
        reporter: '@techrecycle_ve',
        status: 'active'
    },
    {
        id: 'demo-11',
        type: 'domestico',
        size: 'large',
        notes: 'Vertedero municipal crecido - afecta escuela cercana',
        coords: [-68.5959, 7.4816], // Barinas
        date: '2026-03-14',
        reporter: '@padrescuela',
        status: 'active'
    },
    {
        id: 'demo-12',
        type: 'textil',
        size: 'medium',
        notes: 'Ropa y textiles en descomposición al aire libre',
        coords: [-70.2434, 9.0223], // San Felipe
        date: '2026-03-13',
        reporter: '@modasostenible',
        status: 'cleaned'
    },
    {
        id: 'demo-13',
        type: 'plastico',
        size: 'small',
        notes: 'Botella plásticas bloqueando drenaje',
        coords: [-66.6230, 10.4706], // Caracas - Petare
        date: '2026-03-12',
        reporter: '@mipetriofavela',
        status: 'active'
    },
    {
        id: 'demo-14',
        type: 'industrial',
        size: 'large',
        notes: 'Lodos tóxicos de工业区 filtrándose al subsuelo',
        coords: [-72.2034, 10.7234], // Punto Fijo
        date: '2026-03-11',
        reporter: '@petroleovalle',
        status: 'verified'
    },
    {
        id: 'demo-15',
        type: 'domestico',
        size: 'medium',
        notes: 'Basura acumulada en quebrada - riesgo de inundación',
        coords: [-67.0244, 9.7646], // Acarigua
        date: '2026-03-10',
        reporter: '@defensaciudadana',
        status: 'active'
    }
];

// Función para cargar mock data cuando el backend no está disponible
function getMockReports() {
    return MOCK_REPORTS;
}
