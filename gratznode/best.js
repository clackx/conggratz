const express = require('express')
// var cors = require('cors'); 
const db = require('./db');
const { formatData, languages } = require('./misc');

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
    const occuObj = await db.getOccupationsObj(wdEntities)
    const peopleObj = await db.getPeopleObj(wdEntities)
    const flagCntryObj = await db.getFlagCountriesObj(wdEntities)

    const result = formatData({
        'wdEntities': wdEntitiesWRank,
        occuObj, peopleObj, flagCntryObj, lang
    })

    return result
}
