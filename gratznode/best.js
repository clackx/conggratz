const express = require('express')
// var cors = require('cors');
const db = require('./db');
const { formatObject, languages } = require('./misc');
const { cacheEntity, getEntities } = require('./rds');

const app = express()
const port = 3030
const http = require('http').createServer(app)
const io = require('socket.io')(http, {
    path: "/ws/",
    cors: {
        origin: "*", methods: ["GET", "POST"]
    }
});

// app.use(cors())

app.get('/', async (_, response) => {
    response.send('nothing to see here')
})


app.get('/json', async (request, response) => {
    console.log(new Date().toLocaleString(), request.query)
    const bdate = request.query.bdate || '02.01'
    const lang = request.query.lang || 'en'

    const limit = request.query.limit || 3
    const offset = request.query.offset || 0

    const result = await getJSON({ bdate, limit, offset, lang })
    const totalCount = await db.getCount(bdate, lang) || 0
    response.set('X-Total-Count', totalCount);
    response.set('Access-Control-Expose-Headers', 'X-Total-Count')
    response.send(result)
})



io.on('connection', (socket) => {
    console.log(socket.handshake.time + `: Client with id ${socket.id} connected`);

    socket.on('request', async (message) => {
        console.log('Request from', socket.id, message)

        const { day, page, limit, lang } = message
        if (day) {
            const data = await getJSON({ bdate: day, limit, offset: page * limit, lang })
            socket.emit('pageData', data);
        }

        if (page == 0) {
            const totalCount = await db.getCount(day, lang) || 0
            socket.emit('totalCount', totalCount);
        }
    });

    socket.on('disconnect', () => {
        console.log(
            `Client with id ${socket.id} disconnected`
        );
    });
});



http.listen(port, () =>
    console.log(`Server listens on port ${port}.`)
);


async function getJSON({ bdate, limit, offset, lang }) {
    const _offset = offset > 0 ? offset : 0
    const _lang = languages.includes(lang) ? lang : 'en'
    const params = [bdate, limit, _offset]
    const wdEntitiesWRank = await db.getWDEs(params, _lang)
    if (!wdEntitiesWRank?.length) return {}

    const wdEntities = wdEntitiesWRank.map(wde => wde[_lang + 'wde'])
    const ranks = wdEntitiesWRank.map(rank => rank[_lang + 'rank'])

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
            if (wdEntity) {
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
    }
    return result
}
