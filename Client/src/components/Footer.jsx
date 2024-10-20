// eslint-disable-next-line no-unused-vars
import React from "react";
import { motion } from "framer-motion"; 

const Footer = () => {
  return (
    <footer className="border-b border-neutral-900 text-white">
      {/* Container with fade-in effect using Framer Motion */}
      <motion.div
        className="mt-10 border-t border-gray-700 pt-4 pb-4 text-center"
        initial={{ opacity: 0, y: 50 }} // Initial state: hidden and below view
        animate={{ opacity: 1, y: 0 }}  // Animate to visible and centered
        transition={{ duration: 1 }}     // Animation duration: 1 second
      >
        {/* Text with hover animation */}
        <motion.p
          className="text-gray-500"
          whileHover={{ scale: 1.1, color: "#fff" }} // Scale up slightly and change text color on hover
          transition={{ type: "spring", stiffness: 300 }}
        >
          © {new Date().getFullYear()} Sai Koushik. All Rights Reserved.
        </motion.p>
      </motion.div>
    </footer>
  );
}

export default Footer;
