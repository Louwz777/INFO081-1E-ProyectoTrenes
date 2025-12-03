import tkinter as tk
from tkinter import messagebox
import json
import os
from interfaz import settings as config

def ventana_configuracion_generador(parent):
    """
    Abre una ventana para configurar los parámetros del generador gen_BAT.
    Lee y escribe en gen_BAT/config.json.
    """
    
    # Ruta al archivo de configuración
    ruta_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(ruta_raiz, "gen_BAT", "config.json")
    
    # Cargar configuración actual
    defaults = {"intervalo_batida": 15, "hora_apertura": "07:00", "hora_cierre": "20:00"}
    current_config = defaults.copy()
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                current_config.update(json.load(f))
        except Exception:
            pass

    # Crear ventana
    ventana = tk.Toplevel(parent)
    ventana.title("Configuración Generador (gen_BAT)")
    ventana.geometry("400x350")
    ventana.configure(bg=config.COLOR_BLANCO)
    ventana.transient(parent)
    ventana.grab_set()
    
    tk.Label(ventana, text="Configuración del Generador", font=("Arial", 16, "bold"), bg=config.COLOR_BLANCO).pack(pady=20)
    
    frame_form = tk.Frame(ventana, bg=config.COLOR_BLANCO)
    frame_form.pack(pady=10, padx=20, fill=tk.X)
    
    # Intervalo Batida
    tk.Label(frame_form, text="Intervalo de Ráfaga (min):", font=("Arial", 12), bg=config.COLOR_BLANCO).grid(row=0, column=0, sticky="w", pady=10)
    var_intervalo = tk.StringVar(value=str(current_config.get("intervalo_batida")))
    tk.Entry(frame_form, textvariable=var_intervalo, font=("Arial", 12), width=10).grid(row=0, column=1, sticky="e", pady=10)
    
    # Hora Apertura
    tk.Label(frame_form, text="Hora Apertura (HH:MM):", font=("Arial", 12), bg=config.COLOR_BLANCO).grid(row=1, column=0, sticky="w", pady=10)
    var_apertura = tk.StringVar(value=str(current_config.get("hora_apertura")))
    tk.Entry(frame_form, textvariable=var_apertura, font=("Arial", 12), width=10).grid(row=1, column=1, sticky="e", pady=10)
    
    # Hora Cierre
    tk.Label(frame_form, text="Hora Cierre (HH:MM):", font=("Arial", 12), bg=config.COLOR_BLANCO).grid(row=2, column=0, sticky="w", pady=10)
    var_cierre = tk.StringVar(value=str(current_config.get("hora_cierre")))
    tk.Entry(frame_form, textvariable=var_cierre, font=("Arial", 12), width=10).grid(row=2, column=1, sticky="e", pady=10)
    
    def guardar():
        try:
            intervalo = int(var_intervalo.get())
            apertura = var_apertura.get().strip()
            cierre = var_cierre.get().strip()
            
            # Validaciones simples
            if intervalo <= 0:
                raise ValueError("El intervalo debe ser mayor a 0.")
            
            # Guardar en archivo
            new_config = {
                "intervalo_batida": intervalo,
                "hora_apertura": apertura,
                "hora_cierre": cierre
            }
            
            with open(config_path, 'w') as f:
                json.dump(new_config, f, indent=4)
                
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.\nReinicie la simulación para aplicar cambios.")
            ventana.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Valor inválido: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    tk.Button(ventana, text="GUARDAR", command=guardar, bg=config.COLOR_VERDE, fg=config.COLOR_BLANCO, font=("Arial", 12, "bold"), padx=20, pady=5).pack(pady=20)
    
