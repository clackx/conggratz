import React, { useContext, useEffect, useRef, useState } from "react";
import '../styles/App.css'
import PostList from "../components/PersonList";
import PostForm from "../components/PersonForm";
import PersonModal from "../components/ui/modal/PersonModal";
import PersonService from "../API/PersonService";
import Loader from "../components/ui/Loader/BigCoolLoader";
import { AppContext } from "../context";
import { useParams } from "react-router";
import { useFetching } from "../hooks/useFetching";
import { useObserver } from "../hooks/useObserver";
import { getDigitsDate } from "../misc/dates";


function Posts() {
  const params = useParams()
  const { langChosen, dayChosen, setDayChosen, setLoading, } = useContext(AppContext);
  const [persons, setPersons] = useState([])
  const [totalPages, setTotalPages] = useState(3)
  const [page, setPage] = useState(-1)
  const [modalVis, setModalVis] = useState(false)
  const [person, setPerson] = useState()
  const lastElement = useRef()
  const limit = 7
  const [h2, setH2] = useState('3агру3ка...')   

  const [fetchFirst, isFirstLoading, loadFirstError] = useFetching(async (day, lang, limit) => {
    const response = await PersonService.getAll(day, lang, limit, 0);
    setPersons([...response.data])
    const totalCount = response.headers['x-total-count']
    setTotalPages(Math.ceil(parseInt(totalCount) / limit));
    setPage(0)
  })


  const [fetchNext, isNextLoading, loadNextError] = useFetching(async (day, lang, limit, page) => {
    const response = await PersonService.getAll(day, lang, limit, limit * page);
    setPersons(prev => [...prev, ...response.data])
  })


  useObserver(lastElement, page < totalPages, isNextLoading, () => {
    setPage(prev => prev + 1);
  })


  useEffect(() => {
    if (dayChosen) {
      fetchFirst(dayChosen, langChosen, limit)
    }
  }, [dayChosen, langChosen]) // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    if (page > 0) {
      fetchNext(dayChosen, langChosen, limit, page)
    }
  }, [page])                  // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    setDayChosen(getDigitsDate(params.bday, 0))
  }, [params.bday])           // eslint-disable-line react-hooks/exhaustive-deps



  useEffect(() => {
    setLoading(isFirstLoading)
  }, [isFirstLoading])        // eslint-disable-line react-hooks/exhaustive-deps


  useEffect(() => {
    if (loadNextError || loadFirstError) {
      setH2(loadFirstError + ' / ' + loadNextError)
    }
  }, [loadNextError, loadFirstError])


  const showModal = (showperson) => {
    setPerson(showperson)
    setModalVis(true)
  }

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

export default Posts;
