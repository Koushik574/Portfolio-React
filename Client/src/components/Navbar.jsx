import profile from "../assets/profile.png";
import { FaLinkedin, FaGithub, FaTwitterSquare } from "react-icons/fa";

const Navbar = () => {
    return (
        <nav className="mb-20 flex items-center justify-between py-6">
            <div className="flex flex-shrink-0 items-center">
                <img className="mx-2 w-10" src={profile} alt="logo" />
            </div>
            <div className="m-8 flex items-center justify-center gap-4 text-2xl">
                <a href="https://github.com/Koushik574" target="_blank" rel="noopener noreferrer">
                    <FaGithub/>
                </a>
                <a href="https://www.linkedin.com/in/sai-koushik-842843217" target="_blank" rel="noopener noreferrer">
                    <FaLinkedin/>
                </a>
                <a href="https://x.com/koushik574" target="_blank" rel="noopener noreferrer">
                    <FaTwitterSquare/>
                </a>

                <a 
                    href="https://dochub.com/koushiksai574/mqNjP3BVW187dM7R9yGzLk/cit-saikoushik-cse-pdf"
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="px-4 py-1 bg-red-500 text-white rounded hover:bg-blue-700 transition-colors duration-300"
                >
                    Resume
                </a>
            </div>
        </nav>
    );
}

export default Navbar;
