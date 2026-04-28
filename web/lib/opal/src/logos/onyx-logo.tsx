import type { IconProps } from "@opal/types";

const SvgOnyxLogo = ({ size, ...props }: IconProps) => (
  <svg
    height={size}
    viewBox="0 0 64 64"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <circle
      cx="32"
      cy="32"
      r="28"
      fill="none"
      stroke="var(--theme-primary-05)"
      strokeWidth="4"
    />
    <text
      x="32"
      y="48"
      textAnchor="middle"
      fontFamily="Georgia, 'Times New Roman', Times, 'Noto Serif', serif"
      fontStyle="italic"
      fontSize="42"
      fontWeight="700"
      fill="var(--theme-primary-05)"
    >
      i
    </text>
  </svg>
);

export default SvgOnyxLogo;
