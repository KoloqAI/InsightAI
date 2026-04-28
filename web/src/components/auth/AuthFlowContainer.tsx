import Link from "next/link";
import { SvgOnyxLogo } from "@opal/logos";

import AuthShowcase from "./AuthShowcase";

export default function AuthFlowContainer({
  children,
  authState,
  footerContent,
}: {
  children: React.ReactNode;
  authState?: "signup" | "login" | "join";
  footerContent?: React.ReactNode;
}) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background-neutral-00">
      <AuthShowcase />

      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen p-4">
        <div
          className="w-full max-w-md flex items-start flex-col p-6 rounded-16 border border-border-01 shadow-02 backdrop-blur-xl"
          style={{
            backgroundColor:
              "color-mix(in srgb, var(--background-tint-00) 85%, transparent)",
          }}
        >
          <SvgOnyxLogo size={44} className="text-theme-primary-05" />
          <div className="w-full mt-3">{children}</div>
        </div>

        {authState === "login" && (
          <div className="text-sm mt-6 text-center w-full text-text-03 mainUiBody mx-auto">
            {footerContent ?? (
              <>
                New to Insight?{" "}
                <Link
                  href="/auth/signup"
                  className="text-text-05 mainUiAction underline transition-colors duration-200"
                >
                  Create an Account
                </Link>
              </>
            )}
          </div>
        )}
        {authState === "signup" && (
          <div className="text-sm mt-6 text-center w-full text-text-03 mainUiBody mx-auto">
            Already have an account?{" "}
            <Link
              href="/auth/login?autoRedirectToSignup=false"
              className="text-text-05 mainUiAction underline transition-colors duration-200"
            >
              Sign In
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
