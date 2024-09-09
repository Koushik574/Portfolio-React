import project1 from "../assets/projects/project-1.png";
import project2 from "../assets/projects/project-2.png";

export const HERO_CONTENT = `I am a dedicated full stack developer with a passion for building efficient and scalable web applications. My expertise spans front-end technologies like React and back-end technologies such as Node.js, MySQL, PostgreSQL, and MongoDB. I aim to create innovative solutions that enhance business performance while delivering seamless and engaging user experiences.`;

export const ABOUT_TEXT = `I am a versatile and committed full stack developer, passionate about building efficient and intuitive web applications. With experience in technologies like React, Next.js, Node.js, MySQL, PostgreSQL, and MongoDB, I am always eager to learn and tackle new challenges. My journey in web development stems from a curiosity about how things work, which has grown into a career centered on continuous learning and adaptation. I thrive in collaborative settings and enjoy solving complex problems to deliver top-tier solutions. Beyond coding, I stay active, explore emerging technologies, and contribute to open-source projects.`;

export const EXPERIENCES = [
  {
    year: "01/05/2024 - 31/05/2024 ",
    role: "Full Stack Developer",
    company: "Revamp Academy",
    description: `I joined Reavmp Academy as a Full Stack Developer intern for one month, where I deepened my understanding of web development concepts and built a video calling website.`,
    technologies: ["Javascript", "React.js", "Node.js", "PostgreSQL"],
    certificate:"https://dochub.com/koushiksai574/B5LgrGvR0aejOzaK9MYq6j/revampintern-fullstackdevelopers-pdf",
  },
];

export const PROJECTS = [
  {
    title: "ShopNest",
    image: project1,
    description:
      "A fully functional e-commerce website with features like product listing, product searching and shopping cart",
    technologies: ["React", "Node.js", "PostgreSQL"],
    github: "https://shop-nest-sigma.vercel.app/",
  },
  {
    title: "Vidwave",
    image: project2,
    description:
      "A web application for making video calls, featuring meeting ID creation and a seamless calling experience.",
    technologies: ["React", "Node.js", "Socket.io", "WebRTC"],
    github: "https://vid-wave.vercel.app/",
  },
];

export const CONTACT = {
  email: "koushiksai574@gmail.com",
};
