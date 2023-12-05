Wir haben die Datenauswertung automatisiert mithilfe eines Python-Scripts gemacht (siehe main.py). Für die Diagramme wurde Pyplot verwendet, für das Clustering die Scipy-Bibliothek. Dazu haben wir 
die Daten nach den Fragen aufgeteilt (siehe DataSet-Klasse) und dann für jede Frage ein Balkendiagramm erstellt, 
um einen ersten Überblick über die Daten zu erhalten. Anschließend haben wir die Datenpunkte mit hierarchischem Clustering 
in verschiedenen Cluster eingeteilt. Wir haben uns zu diesem Zweck auch den K-Modes algorithmus angeschaut, 
der für kategorische Daten gedacht ist. Wir haben uns aber dagegen entschieden, 
da es für uns mit hierarchischen Clustering Algorithmus einfacher war herauszulesen, welche Person in welchem Cluster ist.

Wir haben jede Frage als eine Dimension angesehen und die Antwortmöglichkeiten jeweils durchnummeriert. 
Jede Person wird also gewissermassen asl einen 23-dimensionaler Vektor dargestellt, da wir im Datensatz 23 verschiedene Fragen ausgemacht haben.
Unser Ansatz hat jedoch die Schwäche, dass einerseits pro Frage nur eine Antwortmöglichkeit ausgewählt werden kann. Deshalb wurde bei den wenigen Fragen, die mehrere
Antwortmöglichkeiten haben, wurde jeweils nur eine Antwort für das Clustering berücksichtigt. Die Fragen wurden nicht aktiv gewichtet, 
womit theoretisch einem Thema mit mehr Fragen mehr Gewicht gegeben wird, was nicht zwingend der Wichtigkeit des Themas entspricht. 
Je mehr Antwortmöglichkeiten eine Frage hat, desto mehr Gewicht wird ihr jedoch implizit gegeben, da die Distanz zwischen den Datenpunkten größer wird.
Unser Ansatz hat also durchaus Schwächen, jedoch sollte er für das Definieren einer primären und sekundären Persona ausreichen, 
da etwaige Verzerrungen relativ klein ausfallen sollten, sodass sie nicht wirklich eine Auswirkung auf die auswahl der Personas haben sollte.

Wir haben auch mit verscheidenden Distanzmetriken experimentiert, die Ward-Methode hat sich aber als die beste herausgestellt, bzw das generierte Dendrogramm
sah für uns am sinnvollsten aus, da sich hier eine schöne Baumstruktur ergab. Wir haben jedoch keine Scatter-plots erstellt, 
da diese nur für bis zu 3 Dimensionen sinnvoll sind und wir 23 Dimensionen haben.

Dann haben wir die Balkendiagramme entsprechend den Clustern gefärbt. Dadurch konnten wir sehen, dass die Cluster sich in 
den meisten Fällen gut voneinander unterscheiden, was bedeutet, dass die Cluster einigermaßen sinnvoll sind.
Wir haben mit verschieden vielen Clustern experimentiert und uns dann für 5 Cluster entschieden, da wir der Meinung waren, 
dass dies beim Lesen der Diagramme am sinnvollsten ist. Da die Cluster hierarchisch berechnet werden, wird ja be mehr Clustern 
ohnehin nur die bestehenden Cluster weiter unterteilt, und nicht grundlegend andere Cluster gebildet.

Basierend auf den Clustern haben wir dann die primäre und sekundäre Persona definiert. 
Ausschlaggebend für die primäre Persona war vor allem die grösse des Clusters, da diese einen möglichst grossen Teil der potenziellen App-Nutzer abbilden soll. 
Deshalb haben wir üns für das zweite Cluster (in den Balkendiagrammen orange, im Dendrogramm grün) entschieden.
Bei der sekundären Persona war natürlich wieder die grösse des Clusters wichtig, aber auch die Unterschiede zum ersten Cluster. Hier ist unsere Wahl auf das vierte Cluster (in den Balkendiagrammen rot, im Dendrogramm violett) gefallen.
Dieses ist das zweitgrösste Cluster und unterscheidet sich nicht komplett von der primären Persona, ist z.B. in der Mehrheit aber weiblich, im Gegensatz zu männlichen primären Persona.

Die Eigenschaften der primären Persona ändert sich bei einer anderen Anzahl an Clustern nicht grundlegend, was aus unserer Sicht für eine gute Wahl spricht.



