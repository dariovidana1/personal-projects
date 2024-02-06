import SwiftUI
import RealityKit
import AVFoundation

class AudioViewModel: ObservableObject {
    private var audioPlayer: AVAudioPlayer?

    init() {
        playBackgroundMusic()
    }

    func playBackgroundMusic() {
        guard let url = Bundle.main.url(forResource: "gatita", withExtension: "mp3") else {
            print("Error al cargar el archivo de audio.")
            return
        }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.numberOfLoops = -1 // Repetir indefinidamente
            audioPlayer?.play()
        } catch {
            print("Error al reproducir la canción: \(error.localizedDescription)")
        }
    }
}

struct ARViewContainer: UIViewRepresentable {
    @StateObject private var audioViewModel = AudioViewModel()

    func makeUIView(context: Context) -> ARView {
        let arView = ARView(frame: .zero)

        // Cargar el modelo 3D con animación llamado "baila"
        guard let danceModel = try? Entity.load(named: "baila.usdz") else {
            print("Error al cargar el modelo 3D.")
            return arView
        }

        // Verificar si el modelo tiene animaciones
        if !danceModel.availableAnimations.isEmpty {
            // Seleccionar la primera animación (puedes elegir la que desees)
            let danceAnimation = danceModel.availableAnimations[0]

            // Reproducir la animación
            danceModel.playAnimation(danceAnimation.repeat())
        } else {
            print("El modelo no tiene animaciones.")
        }

        // Envolver el modelo en un AnchorEntity
        let danceAnchor = AnchorEntity()
        danceAnchor.addChild(danceModel)

        // Ajustar la posición o escala según sea necesario
        danceAnchor.scale = SIMD3<Float>(repeating: 0.7)

        // Agregar el modelo a la escena
        arView.scene.addAnchor(danceAnchor)

        return arView
    }

    func updateUIView(_ uiView: ARView, context: Context) {}
}

struct ContentView: View {
    var body: some View {
        ARViewContainer().edgesIgnoringSafeArea(.all)
    }
}

#if DEBUG
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
#endif
