# Architecture

This section describes the high-level architecture of the `` project.

## Languages Detected


- javascript, typescript, markdown, css, json


## API Frameworks


- No API frameworks detected.


## Package Managers


- No package managers detected.


## Config Files


- No config files detected.


## Folder Structure

```mermaid
graph TD

    subgraph .
    
        app -->
    
        public -->
    
        src -->
    
    
        jsconfig.json
    
        postcss.config.mjs
    
        next.config.mjs
    
        copilot-instructions.md
    
        README.md
    
        .gitignore
    
        package-lock.json
    
        package.json
    
        .prettierrc
    
        tsconfig.json
    
    end

    subgraph app
    
        signup -->
    
        components -->
    
        feed -->
    
        login -->
    
    
        layout.js
    
        favicon.ico
    
        page.js
    
        api.js
    
        globals.css
    
    end

    subgraph app/signup
    
    
        page.js
    
    end

    subgraph app/components
    
        filters -->
    
        ui -->
    
        memory -->
    
        chat -->
    
        touch -->
    
        upload -->
    
    
        CedarProvider.js
    
        ClientWrapper.tsx
    
        AuthProvider.js
    
    end

    subgraph app/components/filters
    
    
        FiltersBar.js
    
    end

    subgraph app/components/ui
    
    
        Tag.js
    
    end

    subgraph app/components/memory
    
    
        MemoryCard.js
    
    end

    subgraph app/components/chat
    
    
        ChatPopup.js
    
    end

    subgraph app/components/touch
    
    
        TouchEnabledWrapper.ts
    
    end

    subgraph app/components/upload
    
    
        UploadModal.js
    
    end

    subgraph app/feed
    
    
        constants.js
    
        types.js
    
        page.js
    
    end

    subgraph app/login
    
    
        page.js
    
    end

    subgraph public
    
    
        file.svg
    
        backdrop.png
    
        vercel.svg
    
        next.svg
    
        globe.svg
    
        window.svg
    
        night.png
    
    end

    subgraph src
    
        backend -->
    
        cedar -->
    
    
    end

    subgraph src/backend
    
    
        tags.json
    
    end

    subgraph src/cedar
    
        components -->
    
    
    end

    subgraph src/cedar/components
    
        ui -->
    
        chatMessages -->
    
        chatComponents -->
    
        CommandBar -->
    
        threads -->
    
        voice -->
    
        diffs -->
    
        spells -->
    
        chatInput -->
    
        structural -->
    
        containers -->
    
        text -->
    
        ornaments -->
    
        inputs -->
    
    
    end

    subgraph src/cedar/components/ui
    
    
        tabs.tsx
    
        Slider3D.tsx
    
        KeyboardShortcut.tsx
    
        command.tsx
    
        dialog.tsx
    
        button.tsx
    
        dropdown-menu.tsx
    
    end

    subgraph src/cedar/components/chatMessages
    
        structural -->
    
    
        MultipleChoice.tsx
    
        StreamingText.tsx
    
        Storyline.tsx
    
        CaptionMessages.tsx
    
        StorylineEdge.tsx
    
        MarkdownRenderer.tsx
    
        DialogueOptions.tsx
    
        ChatRenderer.tsx
    
        ChatBubbles.tsx
    
        TodoList.tsx
    
    end

    subgraph src/cedar/components/chatMessages/structural
    
    
        CollapsedChatButton.tsx
    
    end

    subgraph src/cedar/components/chatComponents
    
    
        FloatingCedarChat.tsx
    
        SidePanelCedarChat.tsx
    
        EmbeddedCedarChat.tsx
    
        CedarCaptionChat.tsx
    
    end

    subgraph src/cedar/components/CommandBar
    
    
        getShortcutDisplay.ts
    
        index.ts
    
        CommandBar.tsx
    
    end

    subgraph src/cedar/components/threads
    
    
        ChatThreadController.tsx
    
    end

    subgraph src/cedar/components/voice
    
    
        VoiceIndicator.tsx
    
    end

    subgraph src/cedar/components/diffs
    
    
        DiffContainer.tsx
    
        DiffText.tsx
    
    end

    subgraph src/cedar/components/spells
    
    
        RemoveMemorySpell.tsx
    
        RangeSliderSpell.tsx
    
        TooltipMenuSpell.tsx
    
        RadialMenuSpell.tsx
    
        QuestioningSpell.tsx
    
        SliderSpell.tsx
    
    end

    subgraph src/cedar/components/chatInput
    
    
        ContextBadgeRow.tsx
    
        HumanInTheLoopIndicator.tsx
    
        ChatInput.css
    
        index.ts
    
        FloatingChatInput.tsx
    
        ChatInput.tsx
    
    end

    subgraph src/cedar/components/structural
    
    
        FloatingContainer.tsx
    
        SidePanelContainer.tsx
    
    end

    subgraph src/cedar/components/containers
    
    
        Flat3dContainer.tsx
    
        Container3D.tsx
    
        Flat3dButton.tsx
    
        GlassyPaneContainer.tsx
    
        Container3DButton.tsx
    
    end

    subgraph src/cedar/components/text
    
    
        PhantomText.tsx
    
        ShimmerText.tsx
    
        TypewriterText.tsx
    
    end

    subgraph src/cedar/components/ornaments
    
    
        GlowingMesh.tsx
    
        GradientMesh.tsx
    
        GlowingMeshGradient.tsx
    
        InsetGlow.tsx
    
    end

    subgraph src/cedar/components/inputs
    
    
        TooltipMenu.tsx
    
    end

```

## Python Modules Overview

