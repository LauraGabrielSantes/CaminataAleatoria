import sys
import random
import csv
from event import Event
from simulation import Simulation
from caminataAleatoria import CaminataAleatoria


def get_resource_info(resources_file):
    """
    Lee el archivo de recursos y retorna un diccionario
    { recurso: cantidad_de_nodos_que_lo_tienen }
    Solo incluye recursos que SÍ existen en la red.
    """
    resource_counts = {}
    with open(resources_file) as f:
        for line in f:
            resources = [int(x) for x in line.split()]
            for r in resources:
                resource_counts[r] = resource_counts.get(r, 0) + 1
    return resource_counts


def select_random_resource(resource_counts):
    """
    Selecciona un recurso aleatorio de los que existen en al menos un nodo.
    Retorna: (recurso_seleccionado, total_nodos_con_ese_recurso)
    """
    available_resources = list(resource_counts.keys())
    selected = random.choice(available_resources)
    return selected, resource_counts[selected]


def generate_graphs(csv_file):
    """Genera las gráficas a partir del archivo CSV de resultados."""
    try:
        import matplotlib.pyplot as plt

        # Leer resultados
        data = []
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)

        # Agrupar y promediar por (TTL, Walkers)
        plot_data = {}
        for row in data:
            key = (int(row['TTL']), int(row['Walkers']))
            if key not in plot_data:
                plot_data[key] = {'fn': [], 'msgs': []}
            plot_data[key]['fn'].append(float(row['FN_Percent']))
            plot_data[key]['msgs'].append(int(row['Messages']))

        walkers_list = [1, 2, 3]
        ttls_list = [1, 2, 3]

        # ---- Gráfica 1: % Falsos Negativos vs TTL ----
        plt.figure(figsize=(10, 6))
        for walkers in walkers_list:
            ttls = []
            fns = []
            for ttl in ttls_list:
                key = (ttl, walkers)
                if key in plot_data:
                    ttls.append(ttl)
                    avg_fn = sum(plot_data[key]['fn']) / len(plot_data[key]['fn'])
                    fns.append(avg_fn)
            plt.plot(ttls, fns, marker='o', linewidth=2, markersize=8,
                     label=f'{walkers} caminante(s)')

        plt.title('% Falsos Negativos vs Longitud de Caminata', fontsize=14)
        plt.xlabel('Longitud de Caminata (TTL)', fontsize=12)
        plt.ylabel('% Falsos Negativos', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('FN_vs_TTL.png', dpi=150)
        print("  Grafica guardada: FN_vs_TTL.png")

        # ---- Gráfica 2: Mensajes vs TTL ----
        plt.figure(figsize=(10, 6))
        for walkers in walkers_list:
            ttls = []
            msgs = []
            for ttl in ttls_list:
                key = (ttl, walkers)
                if key in plot_data:
                    ttls.append(ttl)
                    avg_msgs = sum(plot_data[key]['msgs']) / len(plot_data[key]['msgs'])
                    msgs.append(avg_msgs)
            plt.plot(ttls, msgs, marker='s', linewidth=2, markersize=8,
                    label=f'{walkers} caminante(s)')

        plt.title('Cantidad de Mensajes vs Longitud de Caminata', fontsize=14)
        plt.xlabel('Longitud de Caminata (TTL)', fontsize=12)
        plt.ylabel('Cantidad de Mensajes', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('Messages_vs_TTL.png', dpi=150)
        print("  Grafica guardada: Messages_vs_TTL.png")

        plt.show()

    except ImportError:
        print("\n. Las graficas no se generaron.")
    except Exception as e:
        print(f"\nError al generar graficas: {e}")


def main():

    if len(sys.argv) != 3:
        print("Uso: python3 main.py grafo.txt recursos.txt")
        print("  Ej: python3 main.py grafo200Nodos.txt resourcesForNodes200.txt")
        raise SystemExit(1)

    graph_file = sys.argv[1]
    resources_file = sys.argv[2]

    resource_counts = get_resource_info(resources_file)
    resource_to_find, total_with_resource = select_random_resource(resource_counts)


    print("  EVALUADOR DEL ALGORITMO ABCA (Caminata Aleatoria)")

    print(f"  Grafo:     {graph_file}")
    print(f"  Recursos:  {resources_file}")
    print(f"  Recurso a buscar: {resource_to_find}")
    print(f"  Nodos que lo tienen: {total_with_resource} de {len(resource_counts)} nodos con recursos")

    walk_lengths = [1, 2, 3]
    num_walkers_list = [1, 2, 3]
    trials = 10

    csv_file = 'evaluation_results.csv'


    print(f"\nIniciando evaluacion: {len(walk_lengths)} TTLs × {len(num_walkers_list)} caminantes × {trials} trials = {len(walk_lengths) * len(num_walkers_list) * trials} ejecuciones\n")

    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TTL', 'Walkers', 'Trial', 'FN_Percent', 'Messages', 'Found'])

        total_executions = len(walk_lengths) * len(num_walkers_list) * trials
        current_execution = 0

        for ttl in walk_lengths:
            for walkers in num_walkers_list:
                print(f"  --- TTL={ttl}, Caminantes={walkers} ---")
                for trial in range(trials):
                    current_execution += 1
                    if trial == 0:
                        print(f"     Trial {trial+1}/{trials}...", end='', flush=True)
                    else:
                        print(f" {trial+1}/{trials}...", end='', flush=True)

                    # Crear simulación 
                    maxtime = ttl * 10 + 10
                    experiment = Simulation(graph_file, maxtime, resources_file)
                    # Asignar modelo a cada nodo
                    for i in range(1, len(experiment.graph) + 1):
                        m = CaminataAleatoria()
                        experiment.setModel(m, i)
                    # Evento semilla
                    seed = Event("INICIA", 0.0, 1, 1)
                    seed.setWalkingLength(ttl)
                    seed.setWalkers(walkers)
                    seed.setResourcesToFound([resource_to_find])
                    experiment.init(seed)
                    experiment.run()

                    # Recolectar resultados del nodo raíz
                    root_process = experiment.table[1]
                    found_nodes = root_process.model.idFromResourcesFound
                    found_count = len(found_nodes)
                    false_negatives = total_with_resource - found_count
                    fn_percent = (false_negatives / total_with_resource) * 100
                    messages = experiment.engine.returnMessagesCounter()

                    writer.writerow([ttl, walkers, trial, f"{fn_percent:.2f}", messages, found_count])

                print()  

    print(f"\nEvaluacion completada. {current_execution} ejecuciones realizadas.")
    print(f"   Resultados guardados en: {csv_file}")

    print("\nGenerando graficas...")
    generate_graphs(csv_file)

    print(f"\n{'=' * 65}")
    print("  RESUMEN DE EVALUACION")
    print(f"{'=' * 65}")
    print(f"  Recurso buscado:           {resource_to_find}")
    print(f"  Nodos con el recurso:      {total_with_resource}")
    print(f"  Total de ejecuciones:      {current_execution}")
    print(f"  Archivo de resultados:     {csv_file}")
    print(f"  Graficas generadas:        FN_vs_TTL.png, Messages_vs_TTL.png")
    print(f"{'=' * 65}")


if __name__ == "__main__":
    main()
