import { useState, useEffect } from 'react'
import './App.css'
import ContactList from './ContactList'
import ContactForm from './ContactForm'

function App() {
  // state to store contacts
  // example mock contact {"firstName": "Tim", "lastName": "Drake", "email": "timdrake@gmail.com", "id": 1}
  const [contacts, setContacts] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  // store the contact currently editing
  const [currentContact, setCurrentContact] = useState({})

  // get the contacts when component loads in 
  useEffect(() => {
    fetchContacts()
  }, [] )

  // async function to send a request to the backend to fetch contacts
  const fetchContacts = async () => {
    // fetch - by default, sends a GET request to the /contacts endpoint
    const response = await fetch("http://127.0.0.1:5000/contacts")
    // get the json data associated with the response
    const data = await response.json()
    setContacts(data.contacts)
    console.log(data.contacts)
  }

  //function to close the modal
  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({})
  }
  //function to open the modal (for creation)
  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (contact) => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  return (
    <>
      <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate}/>
      <div className="create-button-wrapper">
        <button onClick={openCreateModal}>Create New Contact</button>
      </div>
      { isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <ContactForm existingContact={currentContact} updateCallback={onUpdate}/>
        </div> 
      </div>
      }
    </>
  )
}

export default App
