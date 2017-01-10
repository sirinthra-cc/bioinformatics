import mygene


def entrez_id_search(gene_symbol):
    mg = mygene.MyGeneInfo()
    entrez_id_list = []
    gene_infos = mg.query('symbol:'+gene_symbol, species='human')
    for hit in gene_infos['hits']:
        if 'entrezgene' in hit:
            entrez_id_list.append((hit['entrezgene'], hit['name']))
    return entrez_id_list

# print(entrez_id_search('cdk*'))
# print(entrez_id_search('fam83h'))
# print(entrez_id_search('jijy'))
