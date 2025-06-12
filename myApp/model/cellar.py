### Module pour requête CELLAR (union européennne) via l'endpoint SPARQL*
from SPARQLWrapper import SPARQLWrapper, JSON
SPARQL_ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"
## utilisation des eurovoc https://eur-lex.europa.eu/browse/eurovoc.html?locale=fr



def get_cellar_data(query):
    """
    Exécute une requête SPARQL sur l'endpoint CELLAR et retourne les résultats.
    
    :param query: La requête SPARQL à exécuter.
    :return: Les résultats de la requête au format JSON.
    """
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête SPARQL: {e}")
        return None


#Récupération de la liste des thèmes Eurovoc sous la forme de dictionnaire avec l'identifiant de l'eurovoc 
# et le libellé du thème. (recherche par nom du thème) (pas plus de 15 résultats)
def get_eurovoc_themes(name='aviation'):
    """
    Récupère la liste des thèmes Eurovoc depuis l'endpoint SPARQL.
    
    :return: Un dictionnaire contenant les thèmes Eurovoc avec leur URI et leur libellé.
    """
    query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX eurovoc: <http://eurovoc.europa.eu/ontology#>
    SELECT DISTINCT ?theme ?label WHERE {{
        ?theme a skos:Concept .
        ?theme skos:prefLabel ?label .
        FILTER (CONTAINS(LCASE(?label), "{name.lower()}"))
        FILTER (LANG(?label) = "fr")
        FILTER (STRSTARTS(STR(?theme), "http://eurovoc.europa.eu/"))
    }} LIMIT 15
    """

    
    results = get_cellar_data(query)
    
    if results:
        themes = {result['theme']['value']: result['label']['value'] for result in results['results']['bindings']}
        return themes
    else:
        return {}

def get_details_work_by_eurovoc_uri(eurovoc_uri, limit=15):
    """
    Récupère les détails des works liés à un concept Eurovoc donné (par son URI).
    :param eurovoc_uri: URI Eurovoc (ex: 'http://eurovoc.europa.eu/4505')
    :return: Liste de dictionnaires avec les infos détaillées sur chaque work.
    """
    uris_str = " ".join(f"<{uri}>" for uri in eurovoc_uri)
    query = f"""
    PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?s ?eurovoc ?label ?type ?exp ?title (str(?force) as ?force) 
           (group_concat(DISTINCT str(?date_if);separator=";") as ?dates_if)
           (group_concat(DISTINCT str(?date_ev);separator=";") as ?dates_ev)
           (str(?celex) as ?celex)
           (group_concat(DISTINCT str(?psi);separator=";") as ?psis)
           ?date_document
    WHERE {{
      VALUES ?eurovoc_uri {{ {uris_str} }}
      ?eurovoc_uri skos:narrower* ?eurovoc.
      ?s cdm:work_is_about_concept_eurovoc ?eurovoc.
      ?s cdm:work_has_resource-type ?t.
      

      OPTIONAL {{ ?s cdm:resource_legal_in-force ?force. }}
      OPTIONAL {{ ?s cdm:resource_legal_date_entry-into-force ?date_if. }}
      OPTIONAL {{ ?s cdm:resource_legal_date_end-of-validity ?date_ev. }}
      OPTIONAL {{ ?s cdm:resource_legal_id_celex ?celex. }}
      OPTIONAL {{ ?s cdm:work_date_document ?date_document. }}
      ?s owl:sameAs ?psi.
      FILTER NOT EXISTS {{ ?s a cdm:publication_general }}
      FILTER NOT EXISTS {{
        ?s cdm:resource_legal_id_sector ?sector.
        FILTER(str(?sector) in ('C','6','7','8','9'))
      }}
      ?t skos:prefLabel ?type.
      FILTER(lang(?type)='fr')
      ?eurovoc skos:prefLabel ?label.
      FILTER(lang(?label)='fr')
      ?exp cdm:expression_belongs_to_work ?s.
      ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/FRA>.
      ?exp cdm:expression_title ?title.
    }}
    ORDER BY DESC(?date_document) 
    LIMIT {limit}
    """

    results = get_cellar_data(query)
    works = []
    if results:
        for result in results['results']['bindings']:
            works.append({
                'work_uri': result['s']['value'],
                'eurovoc_uri': result['eurovoc']['value'],
                'eurovoc_label': result['label']['value'],
                'type': result.get('type', {}).get('value', ''),
                'expression': result.get('exp', {}).get('value', ''),
                'title': result.get('title', {}).get('value', ''),
                'force': result.get('force', {}).get('value', ''),
                'dates_if': result.get('dates_if', {}).get('value', ''),
                'dates_ev': result.get('dates_ev', {}).get('value', ''),
                'celex': result.get('celex', {}).get('value', ''),
                'psis': result.get('psis', {}).get('value', ''),
                'date_document': result.get('date_document', {}).get('value', 'N/A')
            })
    return works

def get_work_by_uri(work_uri, limit=100):
    """
    Récupère les détails d'un work spécifique par son URI.
    
    :param work_uri: URI du work (ex: 'http://data.europa.eu/eli/act/2016/679/oj')
    :return: Dictionnaire avec les infos détaillées sur le work.
    """
    query = f"""
        prefix cdm: <http://publications.europa.eu/ontology/cdm#> 
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        select DISTINCT group_concat(DISTINCT str(?eurovoc);separator=";") as ?psis ?type ?exp ?title (str(?force) as ?force) ?date_document
                    ?date_if
                    ?date_ev
                    group_concat(DISTINCT str(?label); separator=";") as ?label
                    group_concat(DISTINCT str(?celex); separator=";") as ?celex
                    group_concat(DISTINCT str(?psi); separator=";") as ?psi where {{
                        <{work_uri}> cdm:work_is_about_concept_eurovoc ?eurovoc.
                        OPTIONAL {{ <{work_uri}> cdm:work_has_resource-type ?type. }}
                        OPTIONAL {{ <{work_uri}> cdm:resource_legal_in-force ?force. }}
                        OPTIONAL {{ <{work_uri}> cdm:resource_legal_date_entry-into-force ?date_if. }}
                        OPTIONAL {{ <{work_uri}> cdm:resource_legal_date_end-of-validity ?date_ev. }}
                        OPTIONAL {{ <{work_uri}> cdm:resource_legal_id_celex ?celex. }}
                        OPTIONAL {{ <{work_uri}> owl:sameAs ?psi. }}
                        OPTIONAL {{ <{work_uri}> cdm:work_date_document ?date_document. }}
                        OPTIONAL {{
                                    ?exp cdm:expression_belongs_to_work <{work_uri}>.
                                    ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/FRA>.
                                    OPTIONAL {{ ?exp cdm:expression_title ?title. }}
                }}
                ?eurovoc skos:prefLabel ?label.
                FILTER(lang(?label)='fr')
        }} limit {limit}
    """

    results = get_cellar_data(query)
    if results and results['results']['bindings']:
        result = results['results']['bindings'][0]
        return {
            'work_uri': work_uri,
            'psis': result.get('psis', {}).get('value', ''),
            'type': result.get('type', {}).get('value', ''),
            'expression': result.get('exp', {}).get('value', ''),
            'title': result.get('title', {}).get('value', ''),
            'force': result.get('force', {}).get('value', ''),
            'date_if': result.get('date_if', {}).get('value', ''),
            'date_ev': result.get('date_ev', {}).get('value', ''),
            'celex': result.get('celex', {}).get('value', ''),
            'psi': result.get('psi', {}).get('value', ''),
            'date_document': result.get('date_document', {}).get('value', 'N/A'),
            'eurovocs': result.get('label', {}).get('value', ''),
        }
    
    return None

def get_works_by_eurovoc_uri(eurovoc_uri, limit=15):
    """
    Récupère les works liés à un concept Eurovoc donné (par son URI).
    
    :param eurovoc_uri: URI Eurovoc (ex: 'http://eurovoc.europa.eu/4505')
    :return: Liste de dictionnaires avec les infos sur chaque work.
    """
    query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?s (SAMPLE(?psi) AS ?psi_sample) (SAMPLE(?title) AS ?title_sample) ?eurovoc ?label (SAMPLE(?date) AS ?date_sample) WHERE {{
          <{eurovoc_uri}> skos:narrower* ?eurovoc.
          ?s cdm:work_is_about_concept_eurovoc ?eurovoc.
          ?eurovoc skos:prefLabel ?label.
          FILTER(lang(?label)='fr')
          ?exp cdm:expression_belongs_to_work ?s.
          ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/FRA>.
          OPTIONAL {{ ?exp cdm:expression_title ?title. }}
          ?s owl:sameAs ?psi.
          OPTIONAL {{ ?s cdm:work_date_document ?date. }}
        }} GROUP BY ?s ?eurovoc ?label
        ORDER BY DESC(?date_sample)
        LIMIT {limit}
    """

    results = get_cellar_data(query)
    works = []
    if results:
        for result in results['results']['bindings']:
            works.append({
                'work_uri': result['s']['value'],
                'psi': result['s']['value'],  # Utilise l'URI du work comme lien
                'title': result.get('title_sample', {}).get('value', ''),
                'date': result.get('date_sample', {}).get('value', 'N/A'),
                'eurovoc_uri': result['eurovoc']['value'],
                'eurovoc_label': result['label']['value']
            })
    return works

# Exemple d'utilisation :
#eurovoc_uri = "http://eurovoc.europa.eu/4505"
#print(get_works_by_eurovoc_uri(eurovoc_uri))
    """
    PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?s (SAMPLE(?psi) AS ?psi_sample) (SAMPLE(?title) AS ?title_sample) ?eurovoc ?label (SAMPLE(?date) AS ?date_sample) (SAMPLE(?in_force) as ?in_force_sample) WHERE {{
          <http://eurovoc.europa.eu/4505> skos:narrower* ?eurovoc.
          ?s cdm:work_is_about_concept_eurovoc ?eurovoc.
          ?eurovoc skos:prefLabel ?label.
          OPTIONAL {{?s cdm:resource_legal_in-force ?in_force}}.
          FILTER(lang(?label)='fr')
          ?exp cdm:expression_belongs_to_work ?s.
          ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/FRA>.
          OPTIONAL {{ ?exp cdm:expression_title ?title. }}
          ?s owl:sameAs ?psi.
          OPTIONAL {{ ?s cdm:work_date_document ?date. }}
        }} GROUP BY ?s ?eurovoc ?label
        ORDER BY DESC(?date_sample)
        LIMIT 15
    """