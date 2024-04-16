import { redirect } from "react-router-dom";
import { deleteContact } from "../contacts";

export async function action({ params }) {
    console.log('destroying...')
    await deleteContact(params.contactId);
    return redirect("/");
}
