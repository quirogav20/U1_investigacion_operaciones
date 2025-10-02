import numpy as np
print("Iniciando")

def simplex(c, A, b, tipo='max'):
    """Método Simplex para maximización o minimización"""
    
    original_tipo = tipo
    
    if tipo == 'min':
        c = [-x for x in c]
        tipo = 'max'
    
    

    m, n = len(A), len(c)
    tabla = np.zeros((m + 1, n + m + 1))
    tabla[:m, :n] = A
    tabla[:m, n:n+m] = np.eye(m)
    tabla[:m, -1] = b
    tabla[-1, :n] = [-x for x in c]
    
    iteracion = 0
    print(f"\n{'='*60}\nMÉTODO SIMPLEX - {original_tipo.upper()}\n{'='*60}")
   
    print("\nTabla inicial:")
    mostrar_tabla(tabla, n, m)
    
    while True:
        
        if np.all(tabla[-1, :-1] >= -1e-10):  
            break
        
        iteracion += 1
        
        col_piv = np.argmin(tabla[-1, :-1])
        
       
        if tabla[-1, col_piv] >= -1e-10:
            break
    
        ratios = []
        for i in range(m):
            if tabla[i, col_piv] > 1e-10:
                ratios.append(tabla[i, -1] / tabla[i, col_piv])
            else:
                ratios.append(np.inf)
        
        if all(r == np.inf for r in ratios):
            print("\n¡Solución no acotada!")
            return None
        
        fila_piv = np.argmin(ratios)
        pivote = tabla[fila_piv, col_piv]
        
        print(f"\nIteración {iteracion}:")
        print(f"  Variable que entra: x{col_piv+1}")
        print(f"  Variable que sale: fila {fila_piv+1}")
        print(f"  Elemento pivote: {pivote:.4f}")
        
        tabla[fila_piv] = tabla[fila_piv] / pivote
        
        for i in range(m + 1):
            if i != fila_piv:
                factor = tabla[i, col_piv]
                tabla[i] = tabla[i] - factor * tabla[fila_piv]
        
        mostrar_tabla(tabla, n, m)
 
    solucion = np.zeros(n)
    for j in range(n):
        col = tabla[:-1, j]
    
        if np.sum(np.abs(col) > 1e-10) == 1:
            idx = np.where(np.abs(col - 1) < 1e-10)[0]
            if len(idx) == 1:
                solucion[j] = tabla[idx[0], -1]
    
    valor_z = tabla[-1, -1]
    if original_tipo == 'min':
        valor_z = -valor_z
    
    print(f"\n{'='*60}\nSOLUCIÓN ÓPTIMA\n{'='*60}")
    for i, val in enumerate(solucion):
        print(f"x{i+1} = {val:.4f}")
    print(f"Z = {valor_z:.4f}")
    print(f"Iteraciones: {iteracion}\n{'='*60}\n")
    
    return solucion, valor_z

def mostrar_tabla(tabla, n, m):
    """Muestra la tabla simplex de forma legible"""
    print("\n" + "-"*60)
   
    header = "Base |"
    for i in range(n):
        header += f"  x{i+1}  |"
    for i in range(m):
        header += f"  s{i+1}  |"
    header += "  RHS  |"
    print(header)
    print("-"*60)
    
   
    for i in range(m):
        fila = f" R{i+1}  |"
        for j in range(n + m + 1):
            fila += f"{tabla[i,j]:6.2f}|"
        print(fila)
    
   
    fila = "  Z   |"
    for j in range(n + m + 1):
        fila += f"{tabla[-1,j]:6.2f}|"
    print(fila)
    print("-"*60)


def main():
    print("="*50)
    print("    MÉTODO SIMPLEX")
    print("="*50)
    
   
    tipo = input("\n¿Deseas MAXIMIZAR o MINIMIZAR? (max/min): ").lower()
    while tipo not in ['max', 'min']:
        tipo = input("Por favor ingresa 'max' o 'min': ").lower()
    
 
    n = int(input("\n¿Cuántas variables tiene el problema?: "))
    m = int(input("¿Cuántas restricciones tiene el problema?: "))
    
   
    print(f"\nIngresa los coeficientes de la función objetivo Z:")
    c = []
    for i in range(n):
        coef = float(input(f"  Coeficiente de x{i+1}: "))
        c.append(coef)
    
   
    print(f"\nIngresa las restricciones (formato: ax₁ + bx₂ + ... ≤ RHS)")
    print("NOTA: Convierte restricciones ≥ a ≤ multiplicando por -1\n")
    A = []
    b = []
    
    for i in range(m):
        print(f"Restricción {i+1}:")
        fila = []
        for j in range(n):
            coef = float(input(f"  Coeficiente de x{j+1}: "))
            fila.append(coef)
        A.append(fila)
        
        rhs = float(input(f"  Lado derecho (≤): "))
        b.append(rhs)
        print()
    
    
    resultado = simplex(c, A, b, tipo)
    
    otro = input("¿Deseas resolver otro problema . . .? (s/n): ").lower()
    if otro == 's':
        print("\n" * 2)
        main()

if __name__ == "__main__":
    main()
    