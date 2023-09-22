import { createContext, useEffect, useState } from 'react';
import { wsURL } from '../constants';
import { io } from 'socket.io-client';


export const SocketContext = createContext({
  socket: undefined,
  isSocketReady: false,
  socketData: undefined
});

export const SocketProvider = ({ user, children }) => {
  const [isSocketReady, setIsSocketReady] = useState(false);
  const [socketError, setSocketError] = useState(false);
  const [socket, setSocket] = useState();
  const [pageData, setPageData] = useState();
  const [totalCount, setTotalCount] = useState();


  useEffect(() => {

    var socket = io(wsURL,
      {
        path: '/ws/', transports: ['websocket'],
        query: { userId: user.userId }
      })

    setSocket(socket);

    socket.on("connect", () => {
      console.log('Socket connected: socketId', socket.id, 'userId', user.userId)
      setIsSocketReady(true)
    });

    socket.on('connect_error', (err) => {
      const message = 'Socket connection error: ' + err.message
      console.warn(message)
      setSocketError(message)
      setIsSocketReady(false)
    })

    socket.on('connect_failed', (err) => {
      const message = 'Socket connection failed: ' + err.message
      console.warn(message)
      setSocketError(message)
      setIsSocketReady(false)
    })

    socket.on('pageData', (data) => {
      setPageData(data)
    })

    socket.on('totalCount', (count) => {
      setTotalCount(~~(count))
    })

    if (socket.readyState === 1) {
      return () => {
        socket.disconnect();
      }
    }

  }, [user.userId]);


  return (
    <SocketContext.Provider value={{
      socket, isSocketReady, socketError, pageData, totalCount
    }}>
      {children}
    </SocketContext.Provider>
  )

};

