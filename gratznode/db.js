const { Pool } = require('pg');

const pool = new Pool({
    user: 'clackx',
    host: 'localhost',
    database: 'conggratz',
    //   password: 'password',
    port: 5432,
})


async function query(queryString, params) {
    // console.log(queryString, 'WITH', params);
    let result
    try {
        const { rows } = await pool.query(queryString, params);
        result = rows
    } catch (error) {
        console.error(error)
    }
    // console.log('RES:', result.length, 'rows',
    //     JSON.stringify(result).substring(0, 142), '\n')
    return result
}


async function test() {
    return await query("SELECT 1+1")
}


async function getWDEs(params, lang) {
    return await query(
        'SELECT ' + lang + 'wde, ' + lang + 'rank FROM presorted ' +
        'WHERE bday = $1 ORDER BY flyid LIMIT $2 OFFSET $3;', params);
}


async function getCount(bday, lang) {
    const result = await query('SELECT count(*) FROM presorted ' +
        'WHERE bday=$1 AND ' + lang + 'rank IS NOT NULL;', [bday]);
    if (result.length) return result[0].count
    return 0
}


async function getPeople(array) {
    return query(
        'SELECT * FROM people WHERE wdentity = ANY($1)', [array]);
}


async function getManyOccupations(array) {
    return await query('SELECT * FROM tags JOIN occupations ON ' +
        'occupations.occu_entity = tags.occupation_entity ' +
        'WHERE people_entity = ANY($1) ORDER BY _id', [array]);
}


async function getManyCountries(array) {
    return await query('SELECT * FROM countries JOIN flags ON ' +
        'countries.country_entity = flags.country_entity ' +
        'WHERE people_entity = ANY($1) ORDER BY _id', [array]);
}


async function getPeopleObj(wdEntities) {
    const peopleObj = {}
    const peopleData = await getPeople(wdEntities)
    peopleData.map(person => peopleObj[person['wdentity']] = person)
    return peopleObj
}

async function getOccupationsObj(wdEntities) {
    return objFROMData(await getManyOccupations(wdEntities))
}

async function getFlagCountriesObj(wdEntities) {
    return objFROMData(await getManyCountries(wdEntities))
}


const objFROMData = (data) => {
    const r = {}
    data.map(d => r[d.people_entity] = [...r[d.people_entity] || [], d])
    return r
}


module.exports = {
    getWDEs,
    getCount,
    getPeopleObj,
    getOccupationsObj,
    getFlagCountriesObj
}
