# Proyecto de Simulación
 
## Integrantes:
- Carla S Pérez Varela.
- Francisco V Suárez Bellón.
### Tema: Simulación de Eventos Discretos, Inventario.

### Objetivo General:

Hacer una serie de simulaciones computacionales donde se pueda observar el comportamiento de un sistema de inventario, con el fin de poder tomar decisiones que permitan resolver problemas como cuellos de botella,sobre estadía de productos, poco espacio de almacenaje interno.

#### Definición de los eventos:
- Llegada a la tienda, un cliente llega a la tienda, si no hay nadie siendo atendido por el empleado, esté pasará al evento atendido, en caso contrario espera en la cola hasta que llegue su turno.(Es generado por una variable aleatoria con distribución exponencial).
- Tiempo de tramitación del pedido, este evento es el tiempo que debe esperar el cliente desde que hace el pedido al empleado, hasta que recibe el producto y desocupa al empleado, en caso de no poder vender por falta de stock, los tiempos son diferentes, (Para ello se tiene una distribución uniforme). 
- Reabastecimiento, después que es tratado cada cliente se llama a la función de control de stock para conocer si hay que reabastecer, en caso afirmativo, se genera una variable aleatoria con distribución normal para conocer el tiempo que tardará en llegar el pedido, y se reabastece el stock, este evento no es bloqueante del resto de las ventas y solo puede haber uno a la vez.

````mermaid
graph TD;
    A[LLegada a la tienda del cliente]
    B[Se llega a la cola]
    C[El empleado le pide al primero de la cola que realize el pedido y se genera el tiempo de tramitación]
    D[Se espera el pedido y deja disponible para el próximo cliente]
    
    A-->B;
    B-->C;
    C-->D;
    D-->C;
````

### Objetivos Específicos:

 Al realizar la simulación se pueden obtener datos relevantes del sistema como :
- Conocer aproximaciones de la cantidad de clientes que pueden llegar a la tienda.
- Conocer la cantidad de situaciones en que el empleado no puede vender o suplir toda la demanda del cliente y estimar cuanto repercute monetariamente al negocio.
- conocer dada la disponibilidad de empleados cual es el promedio o la mediana de los tiempos de espera, dado que tiempos de espera muy largos pueden causar que los clientes opten por no abandonar la cola o acudir a la competencia en siguientes ocasiones
- Conocer el tiempo promedio que se tarda en reabastecer el stock, para poder tomar decisiones sobre la cantidad de stock que se debe tener en la tienda. Dado que tener un bajo nivel de stock en la tienda en relación con la cantidad de pedidos antes de poder ser reabastecida puede causar cuellos de botella.
- Conocer los intervalos de tiempo en los que la empresa dado que en ocasiones se deben hacer pedidos de reabastecimiento de stock, y estos pueden ser costosos, y se debe tener en cuenta el tiempo que se tarda en reabastecer el stock, para poder tomar decisiones sobre la cantidad de stock que se debe tener en la tienda. Así como conocer que en ciertos momentos el balance puede ser negativo por el bajo volumen de ventas antes del stock lo cual puede ser util para realizar peticiones de préstamos o créditos para estos u optimizar las lineas de tiempo para tratar de mantener el balance en un intervalo deseado.
- Conocer además si la cantidad de stock en la empresa es la adecuada dado que un alto volumen de esta sin ser vendida en una cantidad de tiempo puede causar perdidas a la empresa.

Dado que se realizan N simulaciones independientes donde las semillas de generación de las variables pseudoaleatorias cambian en cada instancia de la simulación con suficientes iteraciones se pueden hacer los análisis estadísticos necesarios para conocer los datos anteriores, brindamos estadígrafos sobre la media aritmetica, mediana, varianza, desviación estandar , máximo y mínimo de los datos
conociendo por ejemplo con respecto a la desviación estandar cuanto difiere la cantidad de clientes atendidos en las simulaciones así como cuantos puieron ser satisfacer su demanda y cuantos no
y cuanto depende esto de la aleatoriedad de los eventos. Además con la mediana se puede conocer donde se concentra el 50% de los cuellos de botellas con el fin de realizar nuevas simulaciones donde esten suplidas estas y ver como se comporta el sistema después de los cambios.
Con los máximos y mínimos podemos ver cuales son los balances que podemos obtener en la línea de tiempo pudiendo asi  adecuar la dirección empresarial y contable a los mejores o peores escenarios posibles asi viendo si el caso promedio es factible empresarialmente, tambien con la distancia entre los datos dado la naturaleza aleatoria de los eventos podemos ver si el sistema es estable o si es muy variable.

### Metodología:

Se deben de realizar N experimentos independientes, osea generando semillas distintas, para garantizar cierto nivel de confianza de los datos, se recomienda que se vaya aumentando los N hasta el punto en que los datos se estabilicen en valores, además de tener ciertos ejemplos de la realidad ayudaría para conocer la cantidad de experimentos necesarios.

Para este caso estimamos que con 1000 experimentos se pueden obtener datos confiables, y se realizarán 10000 experimentos para tener una mayor confianza en los datos.
Y el caso de prueba fue escogido dado que provee un balance final positivo, suficientes clientes (o tiempo en el otro modo) y reabastecimientos que lo pueden asemejar más a la realidad. 
De todos modos nuestro proyecto no solo acepta los valores escogidos sino que puede ponerse a su gusto y se obtendrán todos los datos acompañados de gráficas, aunque por falta de tiempo no se ha podido implementar algún tipo de interfaz visual mas amena y comprensible.

#### Modelación:

En este proyecto se tomó la decisión de realizar la simulación bajo dos enfoques:
- Simular en cuanto a una cantidad máxima de clientes finalizando esta cuanto el último cliente abandone la tienda, siendo el tiempo dependiente hasta que se atienda a la ultima persona.

Este enfoque es factible dado que en ciertos momentos se conoce la cantidad máximas de personas que pueden asistir, dado que se vendió un cierto cupo de accesos a la tienda y se quiere conocer cuanto es el tiempo en atender a todos los clientes.

- Simular en cuanto a una cantidad máxima de tiempo, donde al llegar al límite de esta no se decide dejar llegar a mas clientes, terminando de atender a los que están en cola.
Este enfoque es funcional en situaciones como en las tiendas donde se quiere conocer a que determinado tiempo cerrar para que el último cliente se vaya en un tiempo que no supere la jornada laboral del empleado. 

Nota: Los dos enfoques están en el notebook.

#### Posibles implementaciones del modelo:
Dado el poco tiempo y recursos a mano no es posible implementar todas la ideas que se tienen de esta simulación,
por ello pasamos a explicar que otros resultados pueden extraerse:

- Puede tomarse información sobre las preferencias en una linea de tiempo del producto
- Hacer un análisis sobre las órdenes, pudiendo conocer la cantidad de dinero que puede ser empleado en ellas el tiempo promedio de estas con el fin de conocer si es necesario tomar otro proveedor, en que momentos de tiempo (o aglomeración) se concentra la mediana de estos.
- Aumentar los datos sobre los clientes pudiendo en el caso de la simulación por tiempo conocer cual es la cantidad de pedidos que minimiza la espera, o la cantidad de clientes a los que no se les fue posible satisfacer toda su demanda.
- Realizar distintas simulaciones con conjutos de datos reales para comprobar como el sistema puede adaptarse. 
- Modificar y añadir un evento el cual la tienda debe no poder atender más clientes pero si recibir el reabastecimiento.
- Definir si el reabastecimiento debe ser realizado en un tiempo determinado.

Si el tiempo lo permite realizar una sencilla interfaz web para poder ingreasar los datos y  obtener los datos desados de manera más amena.



# Revisar el notebook para ver el código y los resultados obtenidos.
./Inventory_Proyect/Code/Inventory.ipynb

