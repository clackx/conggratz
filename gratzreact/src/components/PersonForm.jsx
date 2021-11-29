import React, { useContext, useEffect, useState } from "react";
import PersonService from "../API/PersonService";
import { AppContext } from "../context";
import { useFetching } from "../hooks/useFetching";
import DottedLoader from "./ui/Loader/DottedLoader";
import '../styles/Modl.css'

const PersonForm = (props) => {
  const { langCurrent } = useContext(AppContext)
  const [info, setInfo] = useState('')

  var link = ''
  if (props.person) {
    link = props.person.links[langCurrent];
  }

  const [fetchWiki, isWikiLoading, loadWikiError] = useFetching(async (link, lang) => {
    if (link[0] === '*') {
      lang = link.slice(-3, -1)
      link = link.slice(1, -5)
    }
    const response = await PersonService.getWikiInfo(link, lang);
    var info = ''
    const keys = Object.keys(response.data['query']['pages'])
    if (keys.length) {
      info = response.data['query']['pages'][keys[0]]['extract']
    }
    setInfo(info)
  })

  useEffect(() => {
    if (link) {
      setInfo('')
      fetchWiki(link, langCurrent)
    }
  }, [link, langCurrent])  // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setInfo(loadWikiError)
  }, [loadWikiError])

  const getJoined = (list) => {
    var res = ''
    list.map(x => res += x[1][langCurrent] + " " + x[2] + " ")
    return res
  }

  return (
    <form className="formy">
      {props.person
        ? <div className="modldiv">
          <div className="modlphoto">
            <img className="modlimg"
              src={props.person.photo}
              alt="" />
          </div>
          <div className="container">
            <p className="personnamemdl">{props.person.links[langCurrent]}</p>
            <p className="persondescr"> {props.person.descrs[langCurrent]}</p>
            <div style={{ marginTop: 10 }}>
              <p className="personoccus2">
                {getJoined(props.person.occupations.list)}
              </p>
            </div>
            {isWikiLoading &&
            <div className="divloader">
              <DottedLoader /> </div>}
            <p className="persontext">
              {info}
            </p>
          </div>

        </div>
        : <div className="container"><p>noinfo</p></div>}
    </form>
  )
}

export default PersonForm
