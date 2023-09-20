const express = require('express')
// var cors = require('cors');
const db = require('./db');
const { formatObject, languages } = require('./misc');
const { cacheEntity, getEntities } = require('./rds');

const app = express()
const port = 3030

// app.use(cors())

app.get('/', async (_, response) => {
    response.send('nothing to see here')
})


app.get('/json', async (request, response) => {
    console.log(new Date().toLocaleString(), request.query)
    const bdate = request.query.bdate || '02.01'
    let lang = request.query.lang || 'en'
    if (!languages.includes(lang)) lang = 'en'
    const limit = request.query.limit || 3
    const offset = request.query.offset || 0

    const result = await getJSON({ bdate, limit, offset, lang })
    const totalCount = await db.getCount(bdate, lang) || 0
    response.set('X-Total-Count', totalCount);
    response.set('Access-Control-Expose-Headers', 'X-Total-Count')
    response.send(result)
})


app.listen(port, () => {
    console.log(`App running on port ${port}.`)
})


async function getJSON({ bdate, limit, offset, lang }) {
    const params = [bdate, limit, offset]
    const wdEntitiesWRank = await db.getWDEs(params, lang)
    const wdEntities = wdEntitiesWRank.map(wde => wde[lang + 'wde'])
    const ranks = wdEntitiesWRank.map(rank => rank[lang + 'rank'])

    if (!wdEntities.length) return {}

    let result = []
    const entitiesToRequest = []
    const cacheResults = await getEntities(wdEntities);

    for (const [index, c] of cacheResults.entries()) {
        if (c) result.push(JSON.parse(c))
        else entitiesToRequest.push(wdEntities[index])
    }

    if (!entitiesToRequest.length) return result

    // if not all entities are cached
    const occuObj = await db.getOccupationsObj(entitiesToRequest)
    const peopleObj = await db.getPeopleObj(entitiesToRequest)
    const flagCntryObj = await db.getFlagCountriesObj(entitiesToRequest)

    for (const [index, c] of cacheResults.entries()) {
        if (c) result.push(JSON.parse(c))
        else {
            const wdEntity = wdEntities[index]
            const data = formatObject({
                wdEntity,
                pageViewRank: ranks[index],
                occupation: occuObj[wdEntity],
                person: peopleObj[wdEntity],
                flagCntry: flagCntryObj[wdEntity],
                lang
            })
            result.push(data)
            cacheEntity(wdEntity, data)
        }
    }
    return result
}
