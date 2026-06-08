/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          DEFAULT: "#f7efe5",
          light: "#fffdf9",
          dark: "#eddece",
        },
        espresso: {
          DEFAULT: "#1a1208",
          light: "#2d2117",
        },
        rust: {
          DEFAULT: "#7a5c3a",
          dark: "#5c4028",
          light: "#9b7a52",
        },
        taupe: {
          DEFAULT: "#9b8a7a",
          dark: "#7a6a5c",
        },
        gold: {
          DEFAULT: "#c9a84c",
          light: "#e8c96d",
          dark: "#a8873a",
        },
        border: "#e8ddd0",
        muted: "#5c5048",
      },
      fontFamily: {
        serif: ["Playfair Display", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        cormorant: ["Cormorant Garamond", "Georgia", "serif"],
      },
      backgroundImage: {
        "hero-gradient": "linear-gradient(135deg, #f7efe5 0%, #fffdfa 60%, #eddece 100%)",
      },
      animation: {
        shimmer: "shimmer 3s linear infinite",
        float: "floatY 4s ease-in-out infinite",
        "float-delayed": "floatY 4.5s ease-in-out infinite 0.8s",
        glint: "glint 3.5s ease-in-out infinite",
        "fade-up": "fadeUp 0.6s ease-out both",
        "scale-in": "scaleIn 0.5s ease-out both",
        "petal-1": "petalDrift 12s linear infinite",
        "petal-2": "petalDrift 16s linear infinite 2s",
        "petal-3": "petalDrift 14s linear infinite 4s",
        "petal-4": "petalDrift 18s linear infinite 1s",
        "petal-5": "petalDrift 13s linear infinite 5s",
        "petal-6": "petalDrift 15s linear infinite 3s",
      },
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "-200% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        floatY: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-14px)" },
        },
        glint: {
          "0%": { transform: "translateX(-100%) skewX(-15deg)", opacity: "0" },
          "40%": { opacity: "0.6" },
          "100%": { transform: "translateX(200%) skewX(-15deg)", opacity: "0" },
        },
        fadeUp: {
          from: { opacity: "0", transform: "translateY(28px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          from: { opacity: "0", transform: "scale(0.93)" },
          to: { opacity: "1", transform: "scale(1)" },
        },
        petalDrift: {
          "0%": { transform: "translateY(-40px) rotate(0deg)", opacity: "0" },
          "10%": { opacity: "0.15" },
          "90%": { opacity: "0.12" },
          "100%": { transform: "translateY(110vh) rotate(400deg)", opacity: "0" },
        },
      },
      transitionTimingFunction: {
        luxury: "cubic-bezier(0.25, 0.46, 0.45, 0.94)",
      },
      aspectRatio: {
        "4/3": "4 / 3",
        "3/4": "3 / 4",
      },
    },
  },
  plugins: [],
};
