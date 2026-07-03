# MIU + Graphiti Knowledge Graph Integration
> Temporal knowledge graph for the Micelio

## Setup
pip install graphiti-core

## Backends
- Neo4j (recommended): neo4j+s://xxx.databases.neo4j.io
- FalkorDB: free local option

## MIU Schema

### Entity Types
- Concepto: D_f, Df_social, complejidad_fractal, dimension_hausdorff
- Paper: DOI, autores, venue, year, claims
- Investigador: nombre, institucion, lineas
- Dataset: nombre, fuente, N_points, dimension_estimada

### Edge Types
- SOPORTA: (Paper)-[:SOPORTA]->(Hipotesis) con relevance_score
- CONTRADICE: (Paper)-[:CONTRADICE]->(Hipotesis)
- CITA: (Paper)-[:CITA]->(Paper)
- MIDE: (Dataset)-[:MIDE]->(Concepto)

## Integration with MIU Relay
When Corpus Backup runs (Sunday 02:00):
1. Export table MIU to JSON
2. Ingest into Graphiti as episodes
3. Query: "What papers support D_f > D_i?"
4. Result: subgraph with temporal validity

## Query Examples
# Find all facts about fractal dimension that were true in 2025
graph.search("fractal dimension inequality", center_node_uuid="D_f")

# Get evolution of hypothesis confidence over time  
graph.get_edges_by_temporal_range(start="2024-01-01", end="2026-07-01")
