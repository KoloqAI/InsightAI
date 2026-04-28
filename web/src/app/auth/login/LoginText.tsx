"use client";

import React, { useContext } from "react";
import { SettingsContext } from "@/providers/SettingsProvider";
import Text from "@/refresh-components/texts/Text";

export default function LoginText() {
  const settings = useContext(SettingsContext);
  const applicationName =
    (settings && settings?.enterpriseSettings?.application_name) || "Insight";

  return (
    <div className="w-full flex flex-col">
      <Text as="p" headingH2 text05>
        Welcome back
      </Text>
      <Text as="p" text03 mainUiMuted>
        Sign in to your {applicationName} workspace
      </Text>
    </div>
  );
}
