/* 
 * Multi-Party Off-The-Record Messaging Library (Experimental)
 *
 * Author: James Corcoran
 * Dept: Computer Engineering and Computer Science
 * JB Speed School of Engineering 
 * University of Louisville, USA
 *
 * Based on the work of Goldberg, et. al.
*/

/* system headers */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <sys/time.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

/* weechat headers */
#include "weechat/weechat-plugin.h"

#include "mpotr_plugin.h"

WEECHAT_PLUGIN_NAME(MPOTR_PLUGIN_NAME);
WEECHAT_PLUGIN_DESCRIPTION(MPOTR_PLUGIN_DESCRIPTION);
WEECHAT_PLUGIN_AUTHOR(MPOTR_PLUGIN_AUTHOR);
WEECHAT_PLUGIN_VERSION(MPOTR_PLUGIN_VERSION);
WEECHAT_PLUGIN_LICENSE(MPOTR_PLUGIN_LICENSE);

struct t_weechat_plugin *weechat_plugin = NULL;

int
xfer_add_cb (void *data, const char *signal, const char *type_data,
             void *signal_data)
{
    struct t_infolist *infolist;
    const char *plugin_name, *plugin_id, *str_type, *str_protocol;
    const char *remote_nick, *local_nick, *charset_modifier, *filename, *proxy;
    int type, protocol, args, port_start, port_end, sock, port;
    const char *weechat_dir;
    char *dir1, *dir2, *filename2, *short_filename, *pos;
    struct stat st;
    struct hostent *host;
    struct sockaddr_in addr;
    socklen_t length;
    struct in_addr tmpaddr;
    unsigned long local_addr;
    unsigned long long file_size;
    struct t_xfer *ptr_xfer;

    /* make C compiler happy */
    (void) data;
    (void) signal;
    (void) type_data;

    if (!signal_data)
    {
        weechat_printf (NULL,
                        _("%s%s: missing arguments (%s)"),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME, "xfer_add");
        return WEECHAT_RC_ERROR;
    }

    infolist = (struct t_infolist *)signal_data;

    if (!weechat_infolist_next (infolist))
    {
        weechat_printf (NULL,
                        _("%s%s: missing arguments (%s)"),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME, "xfer_add");
        return WEECHAT_RC_ERROR;
    }

    filename2 = NULL;
    short_filename = NULL;

    sock = -1;
    port = 0;

    plugin_name = weechat_infolist_string (infolist, "plugin_name");
    plugin_id = weechat_infolist_string (infolist, "plugin_id");
    str_type = weechat_infolist_string (infolist, "type");
    str_protocol = weechat_infolist_string (infolist, "protocol");
    remote_nick = weechat_infolist_string (infolist, "remote_nick");
    local_nick = weechat_infolist_string (infolist, "local_nick");
    charset_modifier = weechat_infolist_string (infolist, "charset_modifier");
    filename = weechat_infolist_string (infolist, "filename");
    proxy = weechat_infolist_string (infolist, "proxy");
    protocol = XFER_NO_PROTOCOL;

    if (!plugin_name || !plugin_id || !str_type || !remote_nick || !local_nick)
    {
        weechat_printf (NULL,
                        _("%s%s: missing arguments (%s)"),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME, "xfer_add");
        goto error;
    }

    type = xfer_search_type (str_type);
    if (type < 0)
    {
        weechat_printf (NULL,
                        _("%s%s: unknown xfer type \"%s\""),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME, str_type);
        goto error;
    }

    if (XFER_IS_FILE(type) && (!filename || !str_protocol))
    {
        weechat_printf (NULL,
                        _("%s%s: missing arguments (%s)"),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME, "xfer_add");
        goto error;
    }

    if (XFER_IS_FILE(type))
    {
        protocol = xfer_search_protocol (str_protocol);
        if (protocol < 0)
        {
            weechat_printf (NULL,
                            _("%s%s: unknown xfer protocol \"%s\""),
                            weechat_prefix ("error"), XFER_PLUGIN_NAME,
                            str_protocol);
            goto error;
        }
    }

    filename2 = NULL;
    file_size = 0;
    port = 0;

    if (type == XFER_TYPE_FILE_RECV)
    {
        filename2 = strdup (filename);
        sscanf (weechat_infolist_string (infolist, "size"), "%llu", &file_size);
    }

    if (type == XFER_TYPE_FILE_SEND)
    {
        /* add home if filename not beginning with '/' or '~' (not for Win32) */
#ifdef _WIN32
        filename2 = strdup (filename);
#else
        if (filename[0] == '/')
            filename2 = strdup (filename);
        else if (filename[0] == '~')
            filename2 = weechat_string_expand_home (filename);
        else
        {
            dir1 = weechat_string_expand_home (weechat_config_string (xfer_config_file_upload_path));
            if (!dir1)
            {
                weechat_printf (NULL,
                                _("%s%s: not enough memory"),
                                weechat_prefix ("error"), XFER_PLUGIN_NAME);
                goto error;
            }

            weechat_dir = weechat_info_get ("weechat_dir", "");
            dir2 = weechat_string_replace (dir1, "%h", weechat_dir);
            if (!dir2)
            {
                weechat_printf (NULL,
                                _("%s%s: not enough memory"),
                                weechat_prefix ("error"), XFER_PLUGIN_NAME);
                free (dir1);
                goto error;
            }
            filename2 = malloc (strlen (dir2) + strlen (filename) + 4);
            if (!filename2)
            {
                weechat_printf (NULL,
                                _("%s%s: not enough memory"),
                                weechat_prefix ("error"), XFER_PLUGIN_NAME);
                free (dir1);
                free (dir2);
                goto error;
            }
            strcpy (filename2, dir2);
            if (filename2[strlen (filename2) - 1] != DIR_SEPARATOR_CHAR)
                strcat (filename2, DIR_SEPARATOR);
            strcat (filename2, filename);
            if (dir1)
                free (dir1);
            if (dir2)
                free (dir2);
        }
#endif
        /* check if file exists */
        if (stat (filename2, &st) == -1)
        {
            weechat_printf (NULL,
                            _("%s%s: cannot access file \"%s\""),
                            weechat_prefix ("error"), XFER_PLUGIN_NAME,
                            filename2);
            if (filename2)
                free (filename2);
            goto error;
        }
        file_size = st.st_size;
    }

    if (XFER_IS_RECV(type))
    {
        sscanf (weechat_infolist_string (infolist, "remote_address"), "%lu", &local_addr);
        port = weechat_infolist_integer (infolist, "port");
    }
    else
    {
        /* get local IP address */
        sscanf (weechat_infolist_string (infolist, "local_address"), "%lu", &local_addr);

        memset (&addr, 0, sizeof (struct sockaddr_in));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl (local_addr);

        /* look up the IP address from network_own_ip, if set */
        if (weechat_config_string(xfer_config_network_own_ip)
            && weechat_config_string(xfer_config_network_own_ip)[0])
        {
            host = gethostbyname (weechat_config_string (xfer_config_network_own_ip));
            if (host)
            {
                memcpy (&tmpaddr, host->h_addr_list[0], sizeof(struct in_addr));
                local_addr = ntohl (tmpaddr.s_addr);

                sock = weechat_infolist_integer (infolist, "socket");
                if (sock > 0)
                {
                    memset (&addr, 0, sizeof (struct sockaddr_in));
                    length = sizeof (addr);
                    getsockname (sock, (struct sockaddr *) &addr, &length);
                    addr.sin_family = AF_INET;
                }
            }
            else
            {
                weechat_printf (NULL,
                                _("%s%s: could not find address for \"%s\", "
                                  "falling back to local IP"),
                                weechat_prefix ("error"), XFER_PLUGIN_NAME,
                                weechat_config_string (xfer_config_network_own_ip));
            }
        }

        /* open socket for xfer */
        sock = socket (AF_INET, SOCK_STREAM, 0);
        if (sock < 0)
        {
            weechat_printf (NULL,
                            _("%s%s: cannot create socket for xfer: error %d %s"),
                            weechat_prefix ("error"), XFER_PLUGIN_NAME,
                            errno, strerror (errno));
            if (filename2)
                free (filename2);
            goto error;
        }

        /* look for port */
        port = 0;

        if (weechat_config_string (xfer_config_network_port_range)
            && weechat_config_string (xfer_config_network_port_range)[0])
        {
            /* find a free port in the specified range */
            args = sscanf (weechat_config_string (xfer_config_network_port_range),
                           "%d-%d", &port_start, &port_end);
            if (args > 0)
            {
                port = port_start;
                if (args == 1)
                    port_end = port_start;

                /* loop through the entire allowed port range */
                while (port <= port_end)
                {
                    if (!xfer_port_in_use (port))
                    {
                        /* attempt to bind to the free port */
                        addr.sin_port = htons (port);
                        if (bind (sock, (struct sockaddr *) &addr, sizeof (addr)) == 0)
                            break;
                    }
                    port++;
                }

                if (port > port_end)
                    port = -1;
            }
        }

        if (port == 0)
        {
            /* find port automatically */
            addr.sin_port = 0;
            if (bind (sock, (struct sockaddr *) &addr, sizeof (addr)) == 0)
            {
                length = sizeof (addr);
                getsockname (sock, (struct sockaddr *) &addr, &length);
                port = ntohs (addr.sin_port);
            }
            else
                port = -1;
        }

        if (port == -1)
        {
            /* Could not find any port to bind */
            weechat_printf (NULL,
                            _("%s%s: cannot find available port for xfer"),
                            weechat_prefix ("error"), XFER_PLUGIN_NAME);
            close (sock);
            if (filename2)
                free (filename2);
            goto error;
        }
    }

    if (XFER_IS_FILE(type))
    {
        /* extract short filename (without path) */
        pos = strrchr (filename2, DIR_SEPARATOR_CHAR);
        if (pos)
            short_filename = strdup (pos + 1);
        else
            short_filename = strdup (filename2);

        /* convert spaces to underscore if asked and needed */
        pos = short_filename;
        while (pos[0])
        {
            if (pos[0] == ' ')
            {
                if (weechat_config_boolean (xfer_config_file_convert_spaces))
                    pos[0] = '_';
            }
            pos++;
        }
    }

    if (type == XFER_TYPE_FILE_RECV)
    {
        if (filename2)
        {
            free (filename2);
            filename2 = NULL;
        }
    }

    /* add xfer entry and listen to socket if type is file or chat "send" */
    if (XFER_IS_FILE(type))
        ptr_xfer = xfer_new (plugin_name, plugin_id, type, protocol,
                             remote_nick, local_nick, charset_modifier,
                             short_filename, file_size, proxy, local_addr,
                             port, sock, filename2);
    else
        ptr_xfer = xfer_new (plugin_name, plugin_id, type, protocol,
                             remote_nick, local_nick, charset_modifier, NULL,
                             0, proxy, local_addr, port, sock, NULL);

    if (!ptr_xfer)
    {
        weechat_printf (NULL,
                        _("%s%s: error creating xfer"),
                        weechat_prefix ("error"), XFER_PLUGIN_NAME);
        close (sock);
        if (short_filename)
            free (short_filename);
        if (filename2)
            free (filename2);
        goto error;
    }

    /* send signal if type is file or chat "send" */
    if (XFER_IS_SEND(ptr_xfer->type) && !XFER_HAS_ENDED(ptr_xfer->status))
        xfer_send_signal (ptr_xfer, "xfer_send_ready");

    if (short_filename)
        free (short_filename);
    if (filename2)
        free (filename2);

    weechat_infolist_reset_item_cursor (infolist);
    return WEECHAT_RC_OK;

error:
    weechat_infolist_reset_item_cursor (infolist);
    return WEECHAT_RC_ERROR;
}


/* callback for command "/mpotr" */

int
mpotr_auth_cb (void *data, const char *signal, const char *type_data, void *signal_data)
{
    struct t_infolist *infolist;
    const char *plugin_name, *plugin_id, *str_type, *str_protocol;
    const char *remote_nick, *local_nick, *charset_modifier, *filename, *proxy;
    int type, protocol, args, port_start, port_end, sock, port;
    const char *weechat_dir;
    char *dir1, *dir2, *filename2, *short_filename, *pos;
//    struct stat st;
    struct hostent *host;
    struct sockaddr_in addr;
    socklen_t length;
    struct in_addr tmpaddr;
    unsigned long local_addr;
    unsigned long long file_size;
    //struct t_xfer *ptr_xfer;
    char temp[50];
    /* make C compiler happy */
    (void) data;
    (void) signal;
    (void) type_data;

    memset (&addr, 0, sizeof (struct sockaddr_in));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl (local_addr);

//    weechat_printf(NULL, address);
    sprintf(temp, "%lu", local_addr);
    weechat_printf(weechat_current_buffer(), temp);

    return WEECHAT_RC_OK;
}

int
weechat_plugin_init (struct t_weechat_plugin *plugin,
                     int argc, char *argv[])
{
    weechat_plugin = plugin;

//    weechat_hook_modifier("irc_in_msg", &wc_in_msg, NULL);
//    weechat_hook_modifier("irc_out_msg", &wc_out_msg, NULL);

    weechat_hook_signal ("mpotr_auth", &mpotr_auth_cb, NULL);

    return WEECHAT_RC_OK;
}

int
weechat_plugin_end (struct t_weechat_plugin *plugin)
{
    /* make C compiler happy */
    (void) plugin;

    return WEECHAT_RC_OK;
}
