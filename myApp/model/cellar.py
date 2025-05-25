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


def get_works_by_eurovoc_uri(eurovoc_uri):
    """
    Récupère les works liés à un concept Eurovoc donné (par son URI).
    
    :param eurovoc_uri: URI Eurovoc (ex: 'http://eurovoc.europa.eu/4505')
    :return: Liste de dictionnaires avec les infos sur chaque work.
    """
    query = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?s ?psi ?title ?eurovoc ?label ?date WHERE {{
        <{eurovoc_uri}> skos:narrower* ?eurovoc.
        ?s cdm:work_is_about_concept_eurovoc ?eurovoc.
        ?eurovoc skos:prefLabel ?label.
        FILTER(lang(?label)='fr')
        ?exp cdm:expression_belongs_to_work ?s.
        ?exp cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/FRA>.
        OPTIONAL {{ ?exp cdm:expression_title ?title. }}
        ?s owl:sameAs ?psi.
        OPTIONAL {{ ?s cdm:work_date_document ?date. }}
        }} ORDER BY DESC(?date)
        LIMIT 15
    """

    results = get_cellar_data(query)
    works = []
    if results:
        for result in results['results']['bindings']:
            works.append({
                'work_uri': result['s']['value'],
                'psi': result['psi']['value'],
                'title': result['title']['value'],
                'date': result.get('date', {}).get('value', 'N/A'),
                'eurovoc_uri': result['eurovoc']['value'],
                'eurovoc_label': result['label']['value']
            })
    return works

# Exemple d'utilisation :
#eurovoc_uri = "http://eurovoc.europa.eu/4505"
#print(get_works_by_eurovoc_uri(eurovoc_uri))