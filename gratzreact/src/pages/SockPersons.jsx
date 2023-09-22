import { customAlphabet } from 'nanoid/non-secure'
import { useState } from "react";
import { SocketProvider } from "../components/SocketProvider";
import { Persons } from "./Persons";


const SockPersons = () => {

  const [userId, setUserId] = useState();
  if (!userId) setUserId(customAlphabet('abcdefghijkmnopqrstuvwxyz023456789', 8)());

  return (
    <SocketProvider user={{ userId }}>
      <Persons />
    </SocketProvider>
  );
}

export default SockPersons 
