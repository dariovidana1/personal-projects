import SwiftUI
import MapKit

struct ContentView: View {
    // Estado para almacenar las direcciones calculadas, controlar la visibilidad de la hoja de direcciones,
    // almacenar las coordenadas seleccionadas y las polilíneas de las rutas.
    @State private var directions: [String] = []
    @State private var showDirections = false
    @State private var selectedCoordinates: [CLLocationCoordinate2D] = []
    @State private var polylines: [MKPolyline] = []

    var body: some View {
        VStack {
            // MapView personalizado para mostrar el mapa y manejar la interacción del usuario.
            MapView(directions: $directions, selectedCoordinates: $selectedCoordinates, polylines: $polylines)

            // Botón para calcular direcciones entre los puntos seleccionados.
            Button(action: {
                self.calculateDirections()
            }, label: {
                Text("Calcular direcciones")
            })
            .disabled(selectedCoordinates.count < 2)
            .padding()

            // Botón para mostrar las direcciones en una hoja modal.
            Button(action: {
                self.showDirections.toggle()
            }, label: {
                Text("Mostrar direcciones")
            })
            .disabled(directions.isEmpty)
            .padding()
        }
        .sheet(isPresented: $showDirections, content: {
            // Hoja modal para mostrar las direcciones calculadas.
            VStack(spacing: 0) {
                Text("Direcciones")
                    .font(.largeTitle)
                    .bold()
                    .padding()

                Divider().background(Color(UIColor.systemBlue))

                List(self.directions, id: \.self) { direction in
                    Text(direction).padding()
                }
            }
        })
    }

    //fuunción para calcular direcciones entre los puntos seleccionados
    private func calculateDirections() {
        guard selectedCoordinates.count >= 2 else { return }

        directions.removeAll()
        polylines.removeAll()

        let group = DispatchGroup() //usar un grupo para sincronizar las solicitudes de direcciones

        for i in 0..<(selectedCoordinates.count - 1) {
            group.enter()

            let request = MKDirections.Request()
            request.source = MKMapItem(placemark: MKPlacemark(coordinate: selectedCoordinates[i]))
            request.destination = MKMapItem(placemark: MKPlacemark(coordinate: selectedCoordinates[i + 1]))
            request.transportType = .automobile

            let directions = MKDirections(request: request)
            directions.calculate { response, error in
                defer { group.leave() }

                if let route = response?.routes.first {
                    self.directions.append(contentsOf: route.steps.map { $0.instructions }.filter { !$0.isEmpty })
                    self.polylines.append(route.polyline)
                }
            }
        }

        group.notify(queue: .main) {
            self.showDirections = !self.directions.isEmpty
        }
    }
}

struct MapView: UIViewRepresentable {
    //estados del ContentView para compartir datos
    @Binding var directions: [String]
    @Binding var selectedCoordinates: [CLLocationCoordinate2D]
    @Binding var polylines: [MKPolyline]

    // Crear un coordinador para manejar las interacciones del mapa
    func makeCoordinator() -> MapViewCoordinator {
        return MapViewCoordinator(self)
    }

    // Crear la vista del mapa y configurar la región inicial y el gesto de toque
    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator

        let region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 25.533547, longitude: -103.408353),
            span: MKCoordinateSpan(latitudeDelta: 0.5, longitudeDelta: 0.5))
        mapView.setRegion(region, animated: true)

        let tapGesture = UITapGestureRecognizer(target: context.coordinator, action: #selector(MapViewCoordinator.mapTapped(_:)))
        mapView.addGestureRecognizer(tapGesture)

        return mapView
    }

    //actualizar la vista del mapa con marcadores y polilíneas
    func updateUIView(_ uiView: MKMapView, context: Context) {
        uiView.removeAnnotations(uiView.annotations)
        for coordinate in selectedCoordinates {
            let annotation = MKPointAnnotation()
            annotation.coordinate = coordinate
            uiView.addAnnotation(annotation)
        }

        uiView.overlays.forEach { uiView.removeOverlay($0) }
        polylines.forEach { uiView.addOverlay($0) }
    }

    //coordinador para manejar las interacciones del mapa y configurar los renderizadores de overlays
    class MapViewCoordinator: NSObject, MKMapViewDelegate {
        var parent: MapView

        init(_ parent: MapView) {
            self.parent = parent
        }

        //toques en el mapa para añadir marcadores y almacenar coordenadas
        @objc func mapTapped(_ gesture: UITapGestureRecognizer) {
            if let mapView = gesture.view as? MKMapView {
                let locationInView = gesture.location(in: mapView)
                let coordinate = mapView.convert(locationInView, toCoordinateFrom: mapView)

                parent.selectedCoordinates.append(coordinate)
                
                let annotation = MKPointAnnotation()
                annotation.coordinate = coordinate
                mapView.addAnnotation(annotation)
            }
        }

        // Configurar el renderizado de las lineas para las rutas.
        func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            if let polyline = overlay as? MKPolyline {
                let renderer = MKPolylineRenderer(polyline: polyline)
                renderer.strokeColor = .systemBlue
                renderer.lineWidth = 5
                return renderer
            }
            return MKOverlayRenderer(overlay: overlay)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
