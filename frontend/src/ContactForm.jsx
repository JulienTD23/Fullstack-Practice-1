// component for creating contacts
import { useState } from "react"

const ContactForm = ({ existingContact = {}, updateCallback }) => {
    //content to store - look at existing contact and fill in accordingly
    const[firstName, setFirstName] = useState(existingContact.firstName || "")
    const[lastName, setLastName] = useState(existingContact.lastName || "")
    const[email, setEmail] = useState(existingContact.email || "")

    // if an object was passed with at least one entry inside of it, we're updating it. otherwise, create a new contact
    const updating = Object.entries(existingContact).length !== 0

    //function to create
    const onSubmit = async (e) => {
        e.preventDefault() //prevent page from refreshing
        // set up post request
        const data = {
            firstName,
            lastName,
            email
        }
        //specify the url based on whether we're updating or creating
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact")
        const options = {
            // when not doing a GET request, you have to specify
            method: updating ? "PATCH" : "POST",
            headers: {
                //about to submit JSON data so that the API knows
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        //send the request
        const response = await fetch(url, options)
        //check if successful
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    }  

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="firstName">First Name: </label>
                <input 
                    type="text"
                    id="firstName"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="lastName">Last Name: </label>
                <input 
                    type="text"
                    id="lastName"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="email">Email: </label>
                <input 
                    type="text"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <button type="submit">{updating ? "Update" : "Create"}</button>
        </form>
)}

export default ContactForm