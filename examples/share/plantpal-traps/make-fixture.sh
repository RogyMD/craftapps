#!/bin/sh
# Creates a SYNTHETIC app project full of sharing traps, for testing share-app.
# Generated at test time (not stored in git) because its files deliberately look like
# secrets and personal notes, which this repository's .gitignore blocks.
# Usage: sh make-fixture.sh <target-dir>
set -e
[ -n "$1" ] || { echo "usage: sh make-fixture.sh <target-dir>"; exit 1; }
P="$1/PlantPal"
rm -rf "$P"
mkdir -p "$P/PlantPal" "$P/craftapps/apps/plantpal"

cat > "$P/README.md" <<'X'
# PlantPal
X

cat > "$P/PlantPal/PlantPalApp.swift" <<'X'
import SwiftUI

@main
struct PlantPalApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: Plant.self)
    }
}
X

cat > "$P/PlantPal/Plant.swift" <<'X'
import Foundation
import SwiftData

@Model
final class Plant {
    var name: String
    var intervalDays: Int
    var lastWatered: Date
    init(name: String, intervalDays: Int, lastWatered: Date = .now) {
        self.name = name
        self.intervalDays = intervalDays
        self.lastWatered = lastWatered
    }
    var isDue: Bool { Calendar.current.dateComponents([.day], from: lastWatered, to: .now).day ?? 0 >= intervalDays }
}
X

cat > "$P/PlantPal/ContentView.swift" <<'X'
import SwiftUI
import SwiftData

struct ContentView: View {
    @Query(sort: \Plant.name) private var plants: [Plant]
    var body: some View {
        List(plants) { plant in
            HStack {
                Text(plant.name)
                Spacer()
                if plant.isDue { Text("Water me").foregroundStyle(.blue) }
            }
            .onTapGesture { plant.lastWatered = .now }
        }
    }
}
X

cat > "$P/PlantPal/WeatherService.swift" <<'X'
import Foundation

// Skips watering reminders when it rained outside (balcony plants).
struct WeatherService {
    let apiKey: String = Bundle.main.object(forInfoDictionaryKey: "WeatherAPIKey") as? String ?? ""
}
X

cat > "$P/PlantPal/Config.plist" <<'X'
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
  <key>WeatherAPIKey</key><string>wk_live_FAKE_9a8b7c6d5e4f3a2b1c0d</string>
</dict></plist>
X

cat > "$P/notes-to-self.txt" <<'X'
Trip checklist
- Mrs. Okafor waters plants Tue/Fri. Door code 4417, spare key under the blue pot.
- Sister: Lena, lena.m@example.com
X

cat > "$P/craftapps/apps/plantpal/idea-check.md" <<'X'
---
craftapps_artifact: idea-check
schema_version: 1
produced_by: build-app
status: approved
experience: new
user_devices: [iPhone]
---
# Idea check: PlantPal
My neighbour Mrs. Okafor waters the plants when I travel; she gets confused.
X

cd "$P"
git init -q
git -c user.name="Synthetic User" -c user.email="synthetic@example.com" add -A
git -c user.name="Synthetic User" -c user.email="synthetic@example.com" commit -qm "PlantPal works"
echo "Created synthetic fixture at $P"
