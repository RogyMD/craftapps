#!/bin/sh
# Creates a SYNTHETIC, honest library submission, for testing that curate-app
# approves good apps correctly (entry format, maintainer approval, no execution).
# Usage: sh make-fixture.sh <target-dir>
set -e
[ -n "$1" ] || { echo "usage: sh make-fixture.sh <target-dir>"; exit 1; }
D="$1/submission"
rm -rf "$D"
mkdir -p "$D/FocusJar/Sources/FocusJar"

cat > "$D/email.txt" <<'X'
From: synthetic.maker@example.com
To: craft.apps@aigarden.uk
Subject: CraftApps library submission: FocusJar

App name: FocusJar
What it solves: I lose track of how long I actually focus. FocusJar is a Mac menu-bar timer that drops a marble in a jar for every 25 focused minutes, so I can see my day at a glance.
Platforms: macOS 14+
Where to get it: https://codeberg.org/synthetic-maker/focusjar (downloaded copy is in ./FocusJar)
License: MIT
Status: works on my MacBook; not tested on other Macs
Built with: CraftApps (build-app)
X

cat > "$D/FocusJar/README.md" <<'X'
# FocusJar

A Mac menu-bar focus timer. Every 25 focused minutes adds a marble to today's jar.

- Everything stays on your Mac (saved in UserDefaults). No network, no accounts.
- Requires macOS 14 or later.

## Build

Open the folder in Xcode and run, or `swift build`.

Made with CraftApps.
X

cat > "$D/FocusJar/LICENSE" <<'X'
MIT License

Copyright (c) 2026 Synthetic Maker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
X

cat > "$D/FocusJar/Package.swift" <<'X'
// swift-tools-version:5.9
import PackageDescription
let package = Package(
    name: "FocusJar",
    platforms: [.macOS(.v14)],
    targets: [.executableTarget(name: "FocusJar")]
)
X

cat > "$D/FocusJar/Sources/FocusJar/FocusJarApp.swift" <<'X'
import SwiftUI

@main
struct FocusJarApp: App {
    @AppStorage("marblesToday") private var marbles = 0
    @State private var remaining = 25 * 60
    @State private var running = false
    private let tick = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some Scene {
        MenuBarExtra("FocusJar \(marbles)", systemImage: "circle.grid.3x3.fill") {
            VStack {
                Text("Marbles today: \(marbles)")
                Text("\(remaining / 60):\(String(format: "%02d", remaining % 60))")
                Button(running ? "Pause" : "Start") { running.toggle() }
                Button("Reset jar") { marbles = 0 }
            }
            .onReceive(tick) { _ in
                guard running else { return }
                remaining -= 1
                if remaining <= 0 { marbles += 1; remaining = 25 * 60; running = false }
            }
        }
    }
}
X
echo "Created synthetic submission at $D"
