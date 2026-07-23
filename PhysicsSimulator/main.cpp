#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <string>

struct Body {
    std::string name;
    double mass;   // In Solar Masses (Sun = 1.0)
    double x, y;   // Coordinates in AU
    double vx, vy; // Velocity vectors in AU/Year
};

int main() {
    // 1. Establish System Units (G = 4 * pi^2)
    const double pi = 3.14159265358979323846;
    const double G = 4.0 * pi * pi; 
    const double dt = 0.0005;        // Smaller time step for high-precision vector collisions
    const int total_steps = 25000;   // Extended loop length to witness orbital drifts. Lower the steps to 25000 for faster computation and quicker validation.

    // 2. Solar System Matrix (Masses converted precisely to Solar Mass units)
    // Sourced directly from NASA Space Science Data Coordinated Archive
    std::vector<Body> system = {
        {"Sun",     1.0,           0.0,     0.0, 0.0,     0.0},
        {"Mercury", 1.6601e-7,     0.387,   0.0, 0.0,     std::sqrt(G * 1.0 / 0.387)},
        {"Venus",   2.4478e-6,     0.723,   0.0, 0.0,     std::sqrt(G * 1.0 / 0.723)},
        {"Earth",   3.0034e-6,     1.000,   0.0, 0.0,     std::sqrt(G * 1.0 / 1.000)},
        {"Mars",    3.2271e-7,     1.524,   0.0, 0.0,     std::sqrt(G * 1.0 / 1.524)},
        {"Jupiter", 9.5479e-4,     5.203,   0.0, 0.0,     std::sqrt(G * 1.0 / 5.203)},
        {"Saturn",  2.8588e-4,     9.537,   0.0, 0.0,     std::sqrt(G * 1.0 / 9.537)},
        {"Uranus",  4.3662e-5,     19.191,  0.0, 0.0,     std::sqrt(G * 1.0 / 19.191)},
        {"Neptune", 5.1513e-5,     30.069,  0.0, 0.0,     std::sqrt(G * 1.0 / 30.069)}
    };

    std::ofstream data_file("solar_system_data.txt");
    if (!data_file.is_open()) {
        std::cerr << "File system access failure.\n";
        return 1;
    }

    std::cout << "Executing O(N^2) Vectorized Gravitational Core...\n";

    // 3. The N-Body Physics Engine Loop
    for (int step = 0; step < total_steps; ++step) {
        
        // Vectors to hold accumulated acceleration for each body this step
        std::vector<double> ax(system.size(), 0.0);
        std::vector<double> ay(system.size(), 0.0);

        // O(N^2) Particle Interaction Matrix Loop
        for (size_t i = 0; i < system.size(); ++i) {
            for (size_t j = 0; j < system.size(); ++j) {
                if (i == j) continue; // A body cannot attract itself

                double dx = system[j].x - system[i].x;
                double dy = system[j].y - system[i].y;
                double r = std::sqrt(dx*dx + dy*dy);

                // Softening factor to prevent infinity errors if objects cross paths closely
                const double softening = 1e-5; 
                double r_softened = std::sqrt(r*r + softening*softening);

                // Newton's law: acceleration on body 'i' due to mass of body 'j'
                ax[i] += (G * system[j].mass * dx) / (r_softened * r_softened * r_softened);
                ay[i] += (G * system[j].mass * dy) / (r_softened * r_softened * r_softened);
            }
        }

        // Apply Euler-Cromer integration step to update ALL bodies (including the Sun)
        for (size_t i = 0; i < system.size(); ++i) {
            system[i].vx += ax[i] * dt;
            system[i].vy += ay[i] * dt;
            system[i].x += system[i].vx * dt;
            system[i].y += system[i].vy * dt;
        }

        // Save positions of ALL objects (including the Sun at index 0)
        for (size_t i = 0; i < system.size(); ++i) {
            data_file << system[i].x << " " << system[i].y << " ";
        }
        data_file << "\n";
    }

    data_file.close();
    std::cout << "N-Body coordinates rendered and cached.\n";
    return 0;
}
