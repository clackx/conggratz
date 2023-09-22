import { useContext, useEffect, useRef, useState } from "react";

import '../styles/App.css'
import PostList from "../components/PersonList";
import PostForm from "../components/PersonForm";
import PersonModal from "../components/ui/modal/PersonModal";
import Loader from "../components/ui/Loader/BigCoolLoader";
import { AppContext } from "../context";
import { useParams } from "react-router";
import { useObserver } from "../hooks/useObserver";
import { getDigitsDate } from "../misc/dates";
import { SocketContext } from "../components/SocketProvider";


export const Persons = () => {
  const params = useParams()
  const { langChosen, dayChosen, setDayChosen, setLoading } = useContext(AppContext);
  const { socket, socketError, pageData, totalCount } = useContext(SocketContext);
  const [persons, setPersons] = useState([])
  const [totalPages, setTotalPages] = useState(3)
  const [page, setPage] = useState(0)
  const [modalVis, setModalVis] = useState(false)
  const [person, setPerson] = useState()
  const lastElement = useRef()
  const limit = 7
  const [h2, setH2] = useState('3агру3ка...')
  const [isNextLoading, setNextLoading] = useState(true)


  useObserver(lastElement, page < totalPages, isNextLoading, () => {
    setPage(prev => prev + 1);
  })


  useEffect(() => {
    if (socket)
      socket.emit('request', { day: dayChosen, lang: langChosen, page: 0, limit })
    setPage(0)
    setPersons([])
    setLoading(true)
    setNextLoading(true)
  }, [dayChosen, langChosen])   // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    if (socket && page > 0)
      socket.emit('request', { day: dayChosen, lang: langChosen, page, limit })
    setNextLoading(true)
  }, [page])                    // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    setDayChosen(getDigitsDate(params.bday, 0))
  }, [params.bday])             // eslint-disable-line react-hooks/exhaustive-deps


  const showModal = (showperson) => {
    setPerson(showperson)
    setModalVis(true)
  }


  useEffect(() => {
    if (socketError) setH2(socketError)
    setNextLoading(false)
  }, [socketError])


  useEffect(() => {
    if (totalCount) setTotalPages(~~(totalCount / limit))
  }, [totalCount])


  useEffect(() => {
    if (pageData) {
      setPersons(prev => [...prev, ...pageData])
      setNextLoading(false)
      setLoading(false)
    }
  }, [pageData])                // eslint-disable-line react-hooks/exhaustive-deps


  return (
    <div className="App">
      <PersonModal visible={modalVis} setVisible={setModalVis}>
        <PostForm person={person} show={setModalVis} />
      </PersonModal>

      <PostList persons={persons} show={showModal} h2={h2} />

      {isNextLoading &&
        <Loader />}

      <div ref={lastElement} />
      <hr className="hrfooter" />
    </div>
  );
}
